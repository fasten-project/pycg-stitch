FROM python:3.9

COPY setup.py ./
COPY pypi-readme.md ./
COPY stitcher ./stitcher
RUN python3 setup.py install

EXPOSE 5000

CMD ["pycg-stitch", "--api"]
