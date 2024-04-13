using System;
using System.IO;
using OfficeOpenXml;

namespace TestModuleSimulator.Writers
{
    /// <summary>
    /// Writes the result to xlsx file.
    /// </summary>
    public class ExcelWriter : Writer
    {
        private readonly string filepath;

        public ExcelWriter(string filepath)
        {
            this.filepath = filepath;

            // Setting up EPPlus license context
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
        }

        public override void Write(DateTime timestamp, string result)
        {
            FileInfo fileInfo = new(filepath);

            using ExcelPackage package = new(fileInfo);
            ExcelWorksheet worksheet;

            // Check if the worksheet exists
            if (package.Workbook.Worksheets.Count == 0)
            {
                // Create a new worksheet
                worksheet = package.Workbook.Worksheets.Add("Results");
                // Add Headers
                worksheet.Cells[1, 1].Value = "Timestamp";
                worksheet.Cells[1, 2].Value = "Result";
            }
            else
            {
                // Use the existing worksheet
                worksheet = package.Workbook.Worksheets[0];
            }

            // Find the next available row
            int newRow = worksheet.Dimension?.Rows + 1 ?? 1;
            if (newRow == 1)
            {
                // If it's still 1, it means the headers were just added
                newRow++;
            }

            // Add data
            worksheet.Cells[newRow, 1].Value = $"{timestamp.ToLongDateString()} {timestamp.ToLongTimeString()}";
            worksheet.Cells[newRow, 2].Value = result;

            // Save to file
            package.Save();
        }
    }
}
