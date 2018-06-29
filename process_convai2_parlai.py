import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='process from parlai format to' 
                                                        ' opennmt-py format')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*', help='convai2'
                                                            'parlai files')
    parser.add_argument('-t', '--test', help='test')
    args = parser.parse_args()

    for input_file_name in args.input_file_names:
        with open(input_file_name) as in_file:
            lines = in_file.readlines()
        chats = []
        for line in lines:
            # will break if we input a file which doesn't start with an example
            if line.startswith('1 '):
                chats.append([line])
            else:
                chats[-1].append(line)
        source_utterances = []
        target_utterances = []
        for chat in chats:
            # The final character of each persona string is random full stop,
            # so we remove it, since everything else has been tokenized (?)
            persona = [line.strip().split(' your persona: ')[1][:-1] for line in 
                        chat if ' your persona: ' in line]
            dialogue = [line.strip().split('\t') for line in chat if ' your persona: ' not in line]
            for line in dialogue:
                # We split and join the line in order to remove the number at 
                # the start of the string
                source = ' '.join(line[0].split(' ')[1:])
                source_utterances.append('\t'.join(persona) + '\t' + source)
                target_utterances.append(line[1])
        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '_source.txt')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(source_utterances))
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '_target.txt')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(target_utterances))


if __name__ == '__main__':
    main()