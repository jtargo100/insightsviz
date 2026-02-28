import json


def render_notebook(notebook_path: str) -> str:
    """Render a Jupyter notebook file to HTML."""
    try:
        import nbformat
        from nbconvert import HTMLExporter

        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        html_exporter = HTMLExporter()
        html_exporter.template_name = 'basic'
        html_exporter.exclude_input_prompt = True
        html_exporter.exclude_output_prompt = True

        body, _ = html_exporter.from_notebook_node(notebook)
        return body
    except ImportError:
        # Fallback: basic rendering without nbconvert
        return render_notebook_basic(notebook_path)
    except Exception as e:
        return f'<div class="alert alert-warning">Error rendering notebook: {e}</div>'


def render_notebook_basic(notebook_path: str) -> str:
    """Basic notebook rendering without nbconvert dependency."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        html_parts = []
        for cell in nb.get('cells', []):
            cell_type = cell.get('cell_type', '')
            source = ''.join(cell.get('source', []))

            if cell_type == 'markdown':
                html_parts.append(f'<div class="nb-cell nb-markdown">{source}</div>')
            elif cell_type == 'code':
                html_parts.append(
                    f'<div class="nb-cell nb-code">'
                    f'<pre><code>{source}</code></pre>'
                    f'</div>'
                )
                # Render outputs
                for output in cell.get('outputs', []):
                    if 'text' in output:
                        text = ''.join(output['text'])
                        html_parts.append(
                            f'<div class="nb-output"><pre>{text}</pre></div>'
                        )
                    elif 'data' in output:
                        data = output['data']
                        if 'text/html' in data:
                            html_parts.append(
                                f'<div class="nb-output">{"".join(data["text/html"])}</div>'
                            )
                        elif 'image/png' in data:
                            html_parts.append(
                                f'<div class="nb-output">'
                                f'<img src="data:image/png;base64,{data["image/png"]}" />'
                                f'</div>'
                            )
                        elif 'text/plain' in data:
                            text = ''.join(data['text/plain'])
                            html_parts.append(
                                f'<div class="nb-output"><pre>{text}</pre></div>'
                            )

        return '\n'.join(html_parts)
    except Exception as e:
        return f'<div class="alert alert-warning">Error rendering notebook: {e}</div>'
