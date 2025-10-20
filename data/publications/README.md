## See /rag_papers_text/ for 42 NVIDIA-affiliated publications
download_arxiv.py 
* calls OpenAlexAPI to access XML metadata of top-cited NVIDIA papers (authors,doi,etc.)
* using doi/links attempt download via OpenAlexAPI or arxiv --> pdf downloads

parse_papers.py
* turns pdf files into .md markdown files for structure
