#!/usr/bin/env python
# coding=utf-8
import xlrd
import xlwt
import json
import os.path
from os import listdir
from os.path import isfile, join

beginrowidx = 3
jsondir = "json/"
xlsdir = "xlsx/"

def getColNames(sheet):
        rowSize = sheet.row_len(0)
        colValues = sheet.row_values(0, 0, rowSize )
        columnNames = []
        counter = 0
        for value in colValues:
                columnNames.append(value)

        return columnNames

def getRowData(row, columnNames):
        rowData = {}
        counter = 0

        for cell in row:
                try:
                        cell.value = int(cell.value)
                except:
                        pass
                rowData[columnNames[counter]] = cell.value
                counter +=1

        return rowData

def getSheetData(sheet, columnNames):
        nRows = sheet.nrows
        sheetData = []
        counter = 1

        for idx in range(1, nRows):
                if idx >= beginrowidx:
                        row = sheet.row(idx)
                        rowData = getRowData(row, columnNames)
                        sheetData.append(rowData)

        return sheetData

def getWorkBookData(workbook):
        nsheets = workbook.nsheets
        counter = 0
        workbookdata = {}

        for idx in range(0, nsheets):
                worksheet = workbook.sheet_by_index(idx)
                columnNames = getColNames(worksheet)
                sheetdata = getSheetData(worksheet, columnNames)
                workbookdata[worksheet.name] = sheetdata

        return workbookdata

def main():
        if not os.path.exists(jsondir):
                os.makedirs(jsondir) 
        
        for filename in listdir(xlsdir):
                filename = xlsdir + filename

                if filename.endswith('.xlsx') or filename.endswith('.xls'):
                        workbook = xlrd.open_workbook(filename)
                        workbookdata = getWorkBookData(workbook)
                        for sheetname in workbookdata :
                                output = open(jsondir + sheetname + ".json", "w", encoding="utf-8")
                                datastring = '{"data":' + json.dumps(workbookdata[sheetname] , sort_keys=True, indent=4,  separators=(',', ": ")) + '}'
                                datastring = datastring.replace('"[','[');
                                datastring = datastring.replace("]\"","]");
                                output.write(datastring)
                                output.close()
                       
main()
