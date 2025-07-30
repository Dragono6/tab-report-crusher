import fitz  # PyMuPDF
import sys

def add_annotations_to_pdf(file_path: str, findings: list, output_path: str):
    """
    Adds highlights and comments to a PDF based on AI findings.
    """
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF for annotation: {e}", file=sys.stderr)
        return

    for finding in findings:
        page_num = finding.get("page", 1) - 1 # PyMuPDF is 0-indexed
        if 0 <= page_num < len(doc):
            page = doc[page_num]
            
            # TODO: Implement robust logic to find the precise location of the issue.
            # This is a placeholder that just searches for the text of the issue.
            issue_text = finding.get("issue", "")
            text_instances = page.search_for(issue_text)

            for inst in text_instances:
                # Add a yellow highlight
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0)) # Yellow
                highlight.update()
                
                # Add a red sticky note comment
                comment_title = "AI Finding"
                comment_text = f"Issue Found: {issue_text}"
                # Position the note near the highlight
                note_pos = fitz.Point(inst.x0, inst.y0 - 20)
                
                annot = page.add_text_annot(note_pos, comment_text, icon="Comment")
                annot.set_info(content=comment_text, title=comment_title)
                annot.set_colors(stroke=(1, 0, 0)) # Red
                annot.update()

    try:
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        print(f"Successfully saved annotated PDF to {output_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error saving annotated PDF: {e}", file=sys.stderr)
    finally:
        doc.close()

# Example Usage (for testing)
if __name__ == '__main__':
    # This is a placeholder for a test.
    # You would need a sample PDF and a sample finding.
    # e.g., add_annotations_to_pdf("sample.pdf", [{"page": 1, "issue": "Design CFM is too low"}], "annotated_sample.pdf")
    pass 