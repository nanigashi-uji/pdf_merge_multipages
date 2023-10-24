#!/bin/env python3
# -*- coding: utf-8; mode: python; -*-
"""
Script for merging multiple pages into single page w/o margin. 
"""
import pypdf
import argparse
import sys
import os
import re
import copy
import math

class FileTypeWithCheck(argparse.FileType):

    def __call__(self, string):
        if string and "w" in self._mode:
            if os.path.exists(string):
                sys.stderr.write(('File: "%s" exists. Is it OK to overwrite? [y/n] : ') % (string))
                sys.stderr.flush()
                ans = sys.stdin.readline().rstrip()
                ypttrn = re.compile(r'^y(es)?$', re.I)
                m = ypttrn.match(ans)
                if not m:
                    sys.stderr.write("Stop file overwriting.\n")
                    sys.exit(1)
                    # raise ValueError('Stop file overwriting')
            if os.path.dirname(string):
                os.makedirs(os.path.dirname(string),
                            exist_ok=True)
        return super().__call__(string)

    def __repr__(self):
        return super().__repr__()

class PDFMarger:

    def __init__(self):
        self.pdfrdrs  = []
        self.inpages  = []
        self.pdfwrtr  = pypdf.PdfWriter()
        self.mrgdinfo = {}
        return

    def page_info(self, pg_obj):
        ul=pg_obj.mediabox.upper_left
        dr=pg_obj.mediabox.lower_right
        wdt = float(dr[0]-ul[0])
        hgt = float(ul[1]-dr[1])
        flg_landscape = (wdt>hgt)
        return (wdt, hgt, flg_landscape)

    def set_metainfo(self, key, val):
        altnames = {'author':   '/Author',
                    'creator':  '/Creator',
                    'producer': '/Producer',
                    'subject':  '/Subject',
                    'title':    '/Title'}
        self.mrgdinfo(altnames.get(key, key), str(val))

    def prepend_metainfo(self, key, val):
        altnames = {'author':   '/Author',
                    'creator':  '/Creator',
                    'producer': '/Producer',
                    'subject':  '/Subject',
                    'title':    '/Title'}
        k = altnames.get(key, key)
        if self.mrgdinfo(k) is not None and len(self.mrgdinfo[k])>0:
            self.mrgdinfo(k, str(val)+' ('+ self.mrgdinfo[k], ')')
        else:            
            self.mrgdinfo(k, str(val))
    
    def merge_documentinfo(self, level='full', title=None):
        if level=='none':
            return
        elif level=='short':
            self.set_metainfo('/Producer', 'pypdf')
            self.set_metainfo('/Creator',  os.path.basename(__file__))
            if title is not None:
                self.prepend_metainfo('/Title', title)
        else: # 'full' or 'partial'
            dlmtr_pttrn = re.compile(r'\s*;\s*')
            buf = {}
            for irdr in self.pdfrdrs:
                iinfo = irdr.metadata
                for k,v in iinfo.items():
                    if v is None or len(v)<=0:
                        continue
                    if buf.get(k) is None:
                        buf[k] = [v]
                    elif v not in buf[k]:
                        buf[k].append(v)

            for k,v in buf.items():
                if level=='partial':
                    if k in ['/CreationDate', '/ModDate']:
                        continue
                    if title is not None and k=='/Title':
                        self.prepend_metainfo('/Title', title)
                        continue
                    
                vlst = dlmtr_pttrn.split('; '.join(v))
                mval = ';'.join(sorted(set(vlst), key=vlst.index))

                if k == '/Producer':
                    self.mrgdinfo[k] = 'pypdf (' + mval + ')'
                elif k == '/Creator':
                    self.mrgdinfo[k] = os.path.basename(__file__) + ' (' + mval + ')'
                elif k=='/Title' and title is not None:
                    self.mrgdinfo[k] = str(title) + ' (' + mval + ')'
                else:
                    self.mrgdinfo[k] = mval
        return
                
    def prep_pdfreader(self, inputs, level='full', title=None):
        for ifobj in inputs:
            irdr   = pypdf.PdfReader(ifobj, strict=False)
            npages = len(irdr.pages)
            self.pdfrdrs.append(irdr)
            for i in range(npages):
                ipg = irdr.pages[i]
                self.inpages.append({'file':   ifobj,
                                     'reader': irdr,
                                     'index':  i,
                                     'dim':    self.page_info(ipg),
                                     'page':   ipg})
        # self.merge_documentinfo(level=level, title=title)

    def merge_pages(self, nh=2, nv=1, order='left2right', rotation='none', halign='none', valign='none'):
        n_ipages  = len(self.inpages)
        n_pp      = nh*nv
        n_mrged,d = divmod(n_ipages, n_pp)

        if d>0:
            n_mrged += 1
        for n_op in range(n_mrged):

            if halign == 'resize':
                if rotation == 'right' or rotation == 'left':
                    owdt = [self.inpages[n_pp*n_op].get('dim')[1]] * nh
                else:                        
                    owdt = [self.inpages[n_pp*n_op].get('dim')[0]] * nh
            else:
                owdt = [0.0] * nh
                
            if valign == 'resize':
                if rotation == 'right' or rotation == 'left':
                    ohgt = [self.inpages[n_pp*n_op].get('dim')[0]] * nv
                else:                        
                    ohgt = [self.inpages[n_pp*n_op].get('dim')[1]] * nv
            else:
                ohgt = [0.0] * nv
                
            ipage_indexes = []


            if rotation == 'right' or rotation == 'left':
                hgt0, wdt0, oflg_landscape = self.inpages[n_pp*n_op].get('dim')
            else:
                wdt0, hgt0, oflg_landscape = self.inpages[n_pp*n_op].get('dim')
            
            for i in range(nh):
                ipage_indexes.append([])
                for j in range(nv):
                    if order=='left2bottom':
                        idx_ipage = n_pp*n_op + i*nv        + (nv-j-1)
                    elif order=='left2top':
                        idx_ipage = n_pp*n_op + i*nv        + j
                    elif order=='right2left':
                        idx_ipage = n_pp*n_op + (nh-i-1)    + (nv-j-1)*nh
                    elif order=='right2bottom':
                        idx_ipage = n_pp*n_op + (nh-i-1)*nv + (nv-j-1)
                    elif order=='right2top':
                        idx_ipage = n_pp*n_op + (nh-i-1)*nv + j
                    else: # default: 'left2right' 
                        idx_ipage = n_pp*n_op + i           + (nv-j-1)*nh
                    
                    if idx_ipage >= n_ipages:
                        ref = self.inpages[n_pp*n_op].get('dim')
                        ipage_indexes[i].append(None)
                    else:
                        ref = self.inpages[idx_ipage].get('dim')
                        ipage_indexes[i].append(idx_ipage)

                    if ((rotation == 'auto'  and ref[2] != oflg_landscape) or
                        (rotation == 'rauto' and ref[2] != oflg_landscape) or
                        rotation == 'right' or rotation == 'left'):
                        hgt, wdt = ref[0:2]
                    else: 
                        wdt, hgt = ref[0:2]

                    if halign=='fit' and wdt0!=float(wdt):
                        hscl=wdt0/float(wdt)
                    else:
                        hscl=1.0
                        
                    if valign=='fit' and hgt0!=float(hgt):
                        vscl=hgt0/float(hgt)
                    else:
                        vscl=1.0

                    if vscl<hscl:
                        scl=vscl
                    else:
                        scl=hscl

                    if halign=='fit':
                        if scl*wdt>owdt[i]:
                            owdt[i] = scl*wdt
                    elif halign != 'resize' and wdt>owdt[i]:
                        owdt[i]=wdt
                        
                    if valign == 'fit':
                        if scl*hgt>ohgt[j]:
                            ohgt[j]=scl*hgt
                    elif valign != 'resize' and hgt>ohgt[j]:
                        ohgt[j]=hgt

            opage = self.pdfwrtr.add_blank_page(width=sum(owdt), height=sum(ohgt))
            for i in range(nh):
                for j in range(nv):
                    if ipage_indexes[i][j] is None:
                        continue

                    hoffset=sum(owdt[0:i])
                    voffset=sum(ohgt[0:j])
                    idx = ipage_indexes[i][j]
                    ipg = self.inpages[idx].get('page')
                    dim = self.inpages[idx].get('dim')
                    rt  = ipg.get('/Rotate') or 0
                    width,height,flg_lndscp = dim[0:3]
                    
                    print(i,j, idx)

                    if (rotation == 'left' or 
                        (rotation == 'auto' and oflg_landscape!=flg_lndscp)):
                        rt += +90
                        height,width = dim[0:2]
                    elif (rotation == 'right' or
                          (rotation == 'rauto' and oflg_landscape!=flg_lndscp)):
                        rt += -90
                        height,width = dim[0:2]
                    elif  rotation == 'flip':
                        rt -= 180
                    else: # Default: 'none'
                        pass

                    if ( halign=='resize' or halign=='fit' ) and owdt[i]!=width:
                        hscale = owdt[i]/float(width)
                    else:
                        hscale = 1.0

                    if ( valign=='resize' or valign=='fit' ) and ohgt[j]!=height:
                        vscale = ohgt[j]/float(height)
                    else:
                        vscale = 1.0

                    if vscale<hscale:
                        scalefctr=vscale
                    else:
                        scalefctr=hscale

                        
                    hgap = float(owdt[i])-scalefctr*float(width)
                    vgap = float(ohgt[j])-scalefctr*float(height)

                    if (rotation == 'left' or 
                        (rotation == 'auto' and oflg_landscape!=flg_lndscp)):
                        hoffset+=scalefctr*width
                    elif (rotation == 'right' or
                          (rotation == 'rauto' and oflg_landscape!=flg_lndscp)):
                        voffset+=scalefctr*height
                    elif  rotation == 'flip':
                        voffset+=scalefctr*height
                        hoffset+=scalefctr*width
                    else: # Default: 'none'
                        pass
                    
                    if vgap>0.0:
                        if valign=='center' or valign=='resize' or valign=='fit':
                            voffset += 0.5*vgap
                        elif valign=='top':
                            voffset += vgap
                    
                    if hgap>0.0:
                        if halign=='center' or halign=='resize' or halign=='fit':
                            hoffset += 0.5*hgap
                        elif halign=='right':
                            hoffset += hgap

                    # Original (Deprecated) code for PyPDF2
                    #opage.mergeRotatedScaledTranslatedPage(page2=ipg, tx=hoffset, ty=voffset,
                    #                                        rotation=rt, scale=scalefctr, expand=False)

                    ipg.add_transformation(pypdf.Transformation().rotate(rotation=rt).translate(tx=hoffset, ty=voffset).scale(sx=scalefctr, sy=scalefctr))

                    ipg_dh = ipg.mediabox.right - ipg.mediabox.left
                    ipg_dv = ipg.mediabox.top   - ipg.mediabox.bottom

                    ipg_ndh = int(math.fabs(scalefctr*math.cos(math.radians(rt))*ipg_dh - math.sin(math.radians(rt))*ipg_dv))
                    ipg_ndv = int(math.fabs(scalefctr*math.cos(math.radians(rt))*ipg_dv + math.sin(math.radians(rt))*ipg_dh))

                    ipg.mediabox.right  = ipg.mediabox.left   + ipg_ndh
                    ipg.mediabox.top    = ipg.mediabox.bottom + ipg_ndv
                    #ipg.mediabox.left   += hoffset
                    ipg.mediabox.right   += hoffset
                    ipg.mediabox.top     += voffset
                    #ipg.mediabox.bottom += voffset
                    opage.merge_page(ipg, expand=False)
        return

    def write(self, ofs):
        self.pdfwrtr.add_metadata(self.mrgdinfo)
        self.pdfwrtr.write(ofs)

def main():
    argpsr = argparse.ArgumentParser(description='Merge multiple mages in PDF files w/o gap.')
    argpsr.add_argument('inputs', metavar='input-file', type=argparse.FileType('rb'),
                        nargs='+', help='Input PDF file(s)')
    argpsr.add_argument('-o', '--output', metavar='filename', type=FileTypeWithCheck('wb'),
                        nargs=1, help='Output file', dest='output', default='a.out.pdf')
    argpsr.add_argument('-c', '--columns', metavar='n_h', type=int,
                        nargs=1, help='# of columns of merged pages (default = 2)', dest='n_x', default=2)
    argpsr.add_argument('-l', '--lines', metavar='n_v', type=int,
                        nargs=1, help='# of lines of merged pages (default = 1)', dest='n_y', default=1)
    argpsr.add_argument('-p', '--page-order', metavar='opt', type=str, nargs=1, dest='order', 
                        choices=['left2right', 'left2bottom', 'left2top', 'right2left', 'right2bottom', 'right2top'],
                        default='left2right', help='Page order (choices=left2right[default], left2bottom, right2left, right2bottom)')
    argpsr.add_argument('-r', '--rotation', metavar='opt', type=str, nargs=1, dest='rotation', 
                        choices=['none', 'flip', 'right', 'left', 'auto', 'rauto'],
                        default='none',
                        help='Page orientation (choices=none[default], flip, right, left, auto, rauto)')
    argpsr.add_argument('-V', '--valign', metavar='opt', type=str, nargs=1, dest='valign', 
                        choices=['resize', 'none', 'top', 'bottom', 'center', 'fit'],
                        default='none', help='Page fitting (choices=resize, none[default], top, bottom, center, fit)')
    argpsr.add_argument('-A', '--align', metavar='opt', type=str, nargs=1, dest='halign', 
                        choices=['resize', 'none', 'right', 'left', 'center', 'fit'],
                        default='none', help='Page fitting (choices=resize, none[default], right, left, center, fit)')
    argpsr.add_argument('-m', '--metainfo', metavar='opt', type=str, nargs=1, dest='metainfo', 
                        choices=['full', 'none', 'partial', 'short'],
                        default='full', help='Meta data for marged file (choices=full[default], none, partial, short)')
    argpsr.add_argument('-t', '-title', metavar='text', type=str, nargs=1, dest='title', 
                        help='set title in meta data for marged file (Default: output file name)')

    args = argpsr.parse_args()
    
    pdfmgr = PDFMarger()
    pdfmgr.prep_pdfreader(args.inputs, level=args.metainfo[0])
    pdfmgr.merge_pages(nh=args.n_x[0], nv=args.n_y[0], 
                       order=args.order[0], rotation=args.rotation[0], valign=args.valign[0], halign=args.halign[0])
    if args.title is not None and args.title[0] is not None and len(args.title[0])>0:
        pdfmgr.merge_documentinfo(level=args.metainfo[0], title=args.title[0])
    else:
        pdfmgr.merge_documentinfo(level=args.metainfo[0], title=args.output[0].name)

    pdfmgr.write(args.output[0])
    
    for ifs in args.inputs:
        ifs.close();
        args.output[0].close()
            
    return

if __name__ == '__main__':
    main()

