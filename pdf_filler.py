from pypdf import PdfReader, PdfWriter

data = {
    "Patient Name": "Juan Dela Cruz",
    "Testing Location": "Baguio City",
    "Date Placed": "08/30/2026",
    "Lot No": "12345",
    "Expiration Date": "12/30/2026",
    "Date Read": "09/01/2026",
    "Induration": "0 mm",

    "Site_Right": "/Yes_xpod"
}


reader = PdfReader("C:\\Users\\Admin\\Desktop\\pdf-form-filler\\pdf_templates\\tb-test-form.pdf")

# print(reader.get_fields())

writer = PdfWriter()
writer.append(reader)

writer.update_page_form_field_values(
    writer.pages[0],
    data
)

with open("completed-form.pdf", "wb") as output:
    writer.write(output)

