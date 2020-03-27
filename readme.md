# Pdf_merge_multipages

Script for layout change of PDF file by merging multiple pages into single page w/o margin.

## Requirement

  - Python: tested with version 2.7
  - PyPDF2: https://pythonhosted.org/PyPDF2/
    - Tested with version 1.26.0 

## Usage

```
usage: pdf_merge_multipages.py [-h] [-output filename] [-columns n_h] [-lines n_v] [-page-order opt]
                               [-rotation opt] [-valign opt] [-align opt] [-metainfo opt] [-title text]
                               input-file [input-file ...]

Merge multiple mages in PDF files w/o gap.

positional arguments:
  input-file        Input PDF file(s)

optional arguments:
  -h, --help        show this help message and exit
  -output filename  Output file
  -columns n_h      # of columns of merged pages (default = 2)
  -lines n_v        # of lines of merged pages (default = 1)
  -page-order opt   Page order (choices=left2right[default], left2bottom, right2left, right2bottom)
  -rotation opt     Page orientation (choices=none[default], flip, right, left, auto, rauto)
  -valign opt       Page fitting (choices=resize, none[default], top, bottom, center, fit)
  -align opt        Page fitting (choices=resize, none[default], right, left, center, fit)
  -metainfo opt     Meta data for marged file (choices=full[default], none, partial, short)
  -title text       set title in meta data for marged file (Default: output file name)
```

## Options

  - `-output filename`: Filename of the output file. (Default: `a.out.pdf`)
  - `-columns nh`, `-lines n_v`: Output page layout. Each pages in input pdf files will be arranged into `n_h` columns × `n_v` lines in a output page. (Default: n_h=2 × n_v=1 ("2up") )
  - `-page-order option`: Order of the sub-Page layout. 
    - `left2right`: Top line will be filled with sub-pages from left to right at first. Then, next lower lines will be filled with sub-pages.
    - `left2bottom`: Most left columns will be filled with sub-pages from top to bottom at first. Then, next right columns will be filled with sub-pages.
    - `left2top`:  Most left columns will be filled with sub-pages from bottom to to at first. Then, next right columns will be filled with sub-pages.
    - `right2left`: Top line will be filled with sub-pages from right to left at first. Then, next lower lines will be filled with sub-pages.
    - `right2bottom`: Most right columns will be filled with sub-pages from top to bottom at first. Then, next left columns will be filled with sub-pages.
    - `right2top`: Most right columns will be filled with sub-pages from bottom to top at first. Then, next left columns will be filled with sub-pages.
  - `-rotation option`: Sub-Page orientation
    - `none`:  Each sub-pages will be located with original orientation. (Default)
    - `flip`:  Each sub-pages will be rotated by 180-deg.
    - `right`: Each sub-pages will be rotated 90-deg counterclockwise.
    - `left`:  Each sub-pages will be rotated 90-deg clockwise.
    - `auto`: If the first sub-page is in an output pageportrait (landscape), only the landscape (portrait) subpages in a same output page will be rotated by 90-deg counterclockwise. 
    - `rauto`:　If the first sub-page in an output page is portrait (landscape), only the landscape (portrait) subpages in a same output page will be rotated by 90-deg clockwise. 
  - `-valign opttion`: Adjustment of vertical position of sub-pages.
    - `none`,`bottom`: Align the bottom of sub-pages for each lines (Default)
    - `center`: Align the vertical center of sub-pages for each lines (Default)
    - `top`: Align the top of sub-pages for each lines (Default)
    - `resize`: Shrink the sub-page size with its height become same as that for the first sub-page in a same output page. If this option is specified with `-algin resize` or `-algin fit`, much smaller scale factor may be applied, but the vertical sub-page spacing is same as the height of the first sub-page in the page. 
    - `fit`: Shrink the sub-page size with its height become same as that for the first sub-page in a same output page. If this option is specified with `-algin resize` or `-algin fit`, much smaller scale factor may be applied, and the vertical sub-page spacing may also become less than the height of the first sub-page in the page. 
  - `-align opttion`: Adjustment of horizontal position of sub-pages.
    - `none`,`left`: Align the right of sub-pages for each columns (Default)
    - `center`: Align the horizontal center of sub-pages for each columns
    - `right`: Align the left of sub-pages for each columns
    - `resize`: Shrink the sub-page size with its width become same as that for the first sub-page in a same output page. If this option is specified with `-valgin resize` or `-valgin fit`, much smaller scale factor may be applied, but the horizontal sub-page spacing is same as the width of the first sub-page in the page. 
    - `fit`: Shrink the sub-page size with its width become same as that for the first sub-page in a same output page. If this option is specified with `-valgin resize` or `-valgin fit`, much smaller scale factor may be applied, and the horizontal sub-page spacing may also become less than the width of the first sub-page in the page. 
  - `-metainfo options`: Meta-data (document info) of output PDF file.
     - `full`: Meta-data will be generated by concatenating the metadata (document info) of input PDF Files. (default)
     - `partial`: Meta-data will be partially generated by concatenating the metadata (document info) of input PDF Files. 
     - `short`: Limted metadata ('/Title'、'/Creater', and '/Producer') will be generated shortly.
     - `none`: No meta-data is generated.(Defalut values of `PyPDF2` will be used.)
  - `-title text`: Specify the title field of the metadata for output PDF file. (Default is the output file name)

## Author
  Nanigashi Uji (53845049+nanigashi-uji@users.noreply.github.com)
 
