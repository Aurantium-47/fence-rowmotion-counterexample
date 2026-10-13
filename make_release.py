"""Check or package only the explicit public file allowlist; standard library only."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check saved hashes without rewriting.')
    args = parser.parse_args()
    names = [s.strip() for s in (ROOT / 'PUBLIC_FILES.txt').read_text(encoding='utf-8').splitlines()
             if s.strip() and not s.startswith('#')]
    if len(names) != len(set(names)) or 'SHA256SUMS' not in names:
        raise ValueError('Invalid or duplicate allowlist entries')
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
            raise ValueError('Every allowlist entry must be a safe relative path')
        actual = ROOT / name
        if actual.is_symlink() or actual.resolve() != ROOT.joinpath(*path.parts).absolute():
            raise ValueError('Symlink or redirected allowlist entry')
        if name != 'SHA256SUMS' and not actual.is_file():
            raise ValueError('Missing allowlisted file: ' + name)
    expected = ''.join(f'{digest(ROOT / name)}  {name}\n' for name in names if name != 'SHA256SUMS')
    hashes = ROOT / 'SHA256SUMS'
    if args.check:
        if hashes.read_text(encoding='utf-8') != expected:
            raise ValueError('Hash mismatch: distributed content has changed')
        print(f'PASS: {len(names) - 1} file hashes; SHA256SUMS excludes itself.')
        return
    with hashes.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(expected)
    target_dir = ROOT / '_release'
    target_dir.mkdir(exist_ok=True)
    target = target_dir / 'W04_fence.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(ROOT / name, 'W04_fence/' + name)
    with zipfile.ZipFile(target) as archive:
        if archive.namelist() != ['W04_fence/' + name for name in names]:
            raise ValueError('Archive allowlist mismatch')
        for name in names:
            if archive.read('W04_fence/' + name) != (ROOT / name).read_bytes():
                raise ValueError('Archive content mismatch: ' + name)
    print(f'PASS: {len(names)} allowlisted files; archive _release/W04_fence.zip')
    print('ZIP_SHA256=' + digest(target))


if __name__ == '__main__':
    main()
