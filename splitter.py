from typing import List
import sys
import os
import glob
from pathlib import Path

import pymupdf


class Splitter:

    def __init__(self, pdf_uri, split_size, from_page, to_page, out_folder='.'):
        self.pdf_uri = pdf_uri
        self.pdf_name = Path(self.pdf_uri).stem
        self.split_size = split_size
        self.out_folder = out_folder
        self.pdf_doc = pymupdf.open(self.pdf_uri)
        self.from_page = from_page
        self.to_page = to_page if to_page is not None else len(self.pdf_doc)
        
        # derived attributes
        self.total_page_count = (self.to_page-self.from_page) + 1
        self.num_full_splits =  self.total_page_count//self.split_size
        self.full_splits_page_count = self.num_full_splits * self.split_size
        self.num_extra_splits = self.total_page_count%self.split_size
        self.num_total_splits = self.num_full_splits if self.num_extra_splits < 1 else self.num_full_splits + 1

        print(self.total_page_count)

    def split_pdf(self)->dict:
        """
        Split pdf as per options provided
        """
        print("Splitting started")
        split_pdf_uris = []
        
        # print(total_page_count, num_full_splits, num_extra_splits)
        for part_num,split_first_page in enumerate(list(range(self.from_page,self.to_page+1,self.split_size))):
            

            x =  split_first_page + self.split_size
            if x > self.to_page: # extra pages territory, crossing splitting bounds
                break
            part_num = part_num+1
            new_pdf = pymupdf.open()
            for page_num in range(split_first_page, x):
                print(f"Page: {page_num}") 
                new_pdf.insert_pdf(self.pdf_doc, from_page=page_num, to_page=page_num)
            split_out_path = os.path.join(self.out_folder, f"{self.pdf_name}-{part_num}.pdf")
            
            new_pdf.save(split_out_path)
            split_pdf_uris.append(split_out_path)
            print(f"PART {part_num}/{self.num_total_splits} Done.")
            new_pdf.close()

        # extras
        if self.num_extra_splits > 0:
           part_num = part_num + 1
           new_pdf = pymupdf.open()
           print("Working on extras")
           start_page = page_num+1
           for page_num in range(start_page, self.to_page+1):
               print(f"Page: {page_num}")
               new_pdf.insert_pdf(self.pdf_doc, from_page=page_num, to_page=page_num)
           split_out_path = os.path.join(self.out_folder, f"{self.pdf_name}-{part_num}.pdf")
           new_pdf.save(split_out_path)
           split_pdf_uris.append(split_out_path)
           print(f"PART {part_num}/{self.num_full_splits+1} Done.")
        print("Splitting complete")
        return split_pdf_uris



