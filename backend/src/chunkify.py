import os

# tries out various ways of chunking up a file, chooses the best one
# currently splits by newlines and then homogenizes the chunks


# chunk length boundaries by number of characters
min_chunk_length = int(os.environ["MIN_CHUNK_LENGTH"])
max_chunk_length = int(os.environ["MAX_CHUNK_LENGTH"])


def chars(text):
    return sum(not c.isspace() for c in text)


def equal_size(text):
    chunk_size = round((min_chunk_length + max_chunk_length) / 2)
    long_chunks = [
        text[start : start + chunk_size] for start in range(0, len(text), chunk_size)
    ]
    return long_chunks


def split_by_newlines(text):
    by_double_newline = text.split("\n\n")
    by_single_newline = [
        [s] if chars(s) < max_chunk_length else s.split("\n") for s in by_double_newline
    ]
    chunks = [line for sublist in by_single_newline for line in sublist]  # flatten
    return chunks


def find_halfway(chunk):
    for pos, c in enumerate(chunk):
        if not c.isspace():
            count = count + 1
        if count > chars(chunk):
            return pos


def split_in_half(chunk):
    count = 0
    pos = find_halfway(chunk)
    return chunk[:pos], chunk[pos:]


def homogenize_chunks(chunks):
    # look through chunks and either split them or attach them to make the sizes fit
    # reversing the order since the assumption is that it's better to attach a small pargraph to its precending oen
    chunks.reverse()
    for index, chunk in enumerate(chunks):
        if chars(chunk) > max_chunk_length:
            part_1, part_2 = split_in_half(chunk)
            chunks[index] = part_1
            chunks.insert(index, part_2)
            chunks.reverse()
            return homogenize_chunks(chunks)
        elif chars(chunk) < min_chunk_length:
            if index == len(chunks):
                chunks[index - 1] = chunk + chunks[index - 1]
                return homogenize_chunks(chunks[: len(chunks) - 1])
            else:
                chunks[index + 1] = chunks[index + 1] + chunk
                chunks.pop(index)
                return homogenize_chunks(chunks)

    # all chunks have right length
    return chunks


def chunkify(text):
    by_newlines = split_by_newlines(text)
    homogenized = homogenize_chunks(by_newlines)
    for c in homogenized:
        print(len(c))
    return homogenized
