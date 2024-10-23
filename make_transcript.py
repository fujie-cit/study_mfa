import os

def run(transcript_file_path: str, start_idx: int, end_idx: int, output_dir_path: str) -> None:
    with open(transcript_file_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.rstrip()
            filename_body, transcript = line.split(':')
            _, idx = filename_body.split('_')
            idx = int(idx)
            if idx < start_idx or idx > end_idx:
                continue

            output_file_path = os.path.join(output_dir_path, filename_body + '.txt')
            with open(output_file_path, 'w') as f_out:
                f_out.write(transcript)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('transcript_file_path', type=str)
    parser.add_argument('start_idx', type=int)
    parser.add_argument('end_idx', type=int)
    parser.add_argument('output_dir_path', type=str)
    args = parser.parse_args()

    run(args.transcript_file_path, args.start_idx, args.end_idx, args.output_dir_path)
