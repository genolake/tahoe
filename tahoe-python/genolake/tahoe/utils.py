
CHR_PREFIX = 'chr'

def formatContig(contig):
    """
    Returns a formatted tuple of contigs. One has trimmed contig, the other appends a 'chr' prefix.

    :param contig: contig with or without 'chr' prefix
    :return: tuple of a trimmed (without 'chr') and full (with 'chr') contig names
    """
    contig_trimmed = contig.lstrip(CHR_PREFIX)

    contig_full = contig if contig.startswith(CHR_PREFIX) else "%s%s" % (CHR_PREFIX, contig)

    return contig_trimmed, contig_full
