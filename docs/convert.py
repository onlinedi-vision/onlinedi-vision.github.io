import json           # for json.load(... endpoints.json file ...)
import os


HTML_HEADER="""
    
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #3498db;
            --secondary-color: #2c3e50;
            --accent-color: #e74c3c;
            --light-color: #ecf0f1;
            --dark-color: #34495e;
            --success-color: #2ecc71;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --gray-light: #f8f9fa;
            --gray: #6c757d;
            --font-main: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--font-main);
            line-height: 1.6;
            color: #333;
            background-color: #f5f7f9;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        header {
            background: linear-gradient(135deg, var(--secondary-color), var(--dark-color));
            color: white;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        header h1 {
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
        }
        
        header p {
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .container {
            display: flex;
            flex: 1;
        }
        
        .sidebar {
            width: 280px;
            background-color: var(--dark-color);
            color: white;
            padding: 1.5rem 0;
            overflow-y: auto;
            height: calc(100vh);
            position: sticky;
            top: 0;
        }
        
        .sidebar h3 {
            padding: 0 1.5rem;
            margin-bottom: 1rem;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .endpoint-list {
            list-style: none;
        }
        
        .endpoint-list li {
            margin-bottom: 0.2rem;
        }
        
        .endpoint-list a {
            display: block;
            padding: 0.8rem 1.5rem;
            color: var(--light-color);
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
        }
        
        .endpoint-list a:hover {
            background-color: rgba(255, 255, 255, 0.1);
            border-left-color: var(--primary-color);
        }
        
        .endpoint-list a.active {
            background-color: rgba(255, 255, 255, 0.15);
            border-left-color: var(--primary-color);
            font-weight: 600;
        }
        
        .main-content {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
        }
        
        .endpoint-section {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            border-left: 5px solid var(--primary-color);
        }
        
        .endpoint-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #eee;
        }
        
        .method {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 4px;
            font-weight: 600;
            margin-right: 1rem;
            font-size: 0.9rem;
        }
        
        .get { background-color: var(--success-color); color: white; }
        .post { background-color: var(--primary-color); color: white; }
        .put { background-color: var(--warning-color); color: white; }
        .delete { background-color: var(--danger-color); color: white; }
        .patch { background-color: #9b59b6; color: white; }
        
        .endpoint-url {
            font-family: monospace;
            font-size: 1.2rem;
            color: var(--dark-color);
            flex: 1;
        }
        
        .endpoint-description {
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }
        
        .parameter-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }
        
        .parameter-table th,
        .parameter-table td {
            padding: 0.8rem 1rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        .parameter-table th {
            background-color: var(--gray-light);
            font-weight: 600;
        }
        
        .parameter-table tr:hover {
            background-color: #f9f9f9;
        }
        
        .code-block {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 1.5rem;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1.5rem 0;
            font-family: 'Fira Code', monospace;
            font-size: 0.95rem;
        }
        
        .code-block pre {
            margin: 0;
        }
        
        .code-key { color: #ff79c6; }
        .code-string { color: #f1fa8c; }
        .code-number { color: #bd93f9; }
        .code-boolean { color: #bd93f9; }
        .code-null { color: #bd93f9; }
        
        .tab-container {
            margin: 1.5rem 0;
        }
        
        .tab-buttons {
            display: flex;
            border-bottom: 1px solid #ddd;
        }
        
        .tab-button {
            padding: 0.8rem 1.5rem;
            background: #f1f1f1;
            border: none;
            cursor: pointer;
            font-weight: 600;
            color: var(--gray);
            transition: all 0.3s ease;
        }
        
        .tab-button.active {
            background: white;
            color: var(--primary-color);
            border-bottom: 3px solid var(--primary-color);
        }
        
        .tab-content {
            padding: 1.5rem;
            background: white;
            border-radius: 0 0 6px 6px;
        }
        
        .tab-pane {
            display: none;
        }
        
        .tab-pane.active {
            display: block;
        }
        
        footer {
            text-align: center;
            padding: 1.5rem;
            background-color: var(--secondary-color);
            color: white;
            margin-top: auto;
        }
        
        .add-endpoint-btn {
            display: block;
            width: calc(100% - 3rem);
            margin: 1rem 1.5rem 0;
            padding: 0.8rem;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
            text-align: center;
            text-decoration: none;
        }
        
        .add-endpoint-btn:hover {
            background-color: #2980b9;
        }
        
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }
            
            .main-content {
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>[od-official-server] API  Documentation</h1>
        <p>Comprehensive guide to using our RESTful API endpoints. </p>
    </header>
    
    <div class="container">
"""
HTML_FOOTER="""
    
        </main>
    </div>
    
    <footer>
        <p>API Documentation &copy; 2023 | Version 1.2.0</p>
    </footer>

    <script>
        function openTab(evt, tabName) {
            // Get all tab content and hide them
            const tabPanes = document.getElementsByClassName("tab-pane");
            for (let i = 0; i < tabPanes.length; i++) {
                tabPanes[i].style.display = "none";
            }
            
            // Get all tab buttons and remove active class
            const tabButtons = document.getElementsByClassName("tab-button");
            for (let i = 0; i < tabButtons.length; i++) {
                tabButtons[i].className = tabButtons[i].className.replace(" active", "");
            }
            
            // Show the current tab and add active class to the button
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        
        // Simple smooth scrolling for navigation
        document.querySelectorAll('.endpoint-list a').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
                
                // Update active class
                document.querySelectorAll('.endpoint-list a').forEach(a => {
                    a.classList.remove('active');
                });
                this.classList.add('active');
            });
        });
    </script>
</body>
</html>"""


def append_html(output: str, stream: File | None) -> None:
    if stream == None:
        print(output)
    else:
        stream.write(output)
    
def append_side_bar(endpoints: list, stream: File | None) -> None:
    side_bar_before="""
       <aside class="sidebar">
            <h3><i class="fas fa-list"></i> Endpoints</h3>
            <ul class="endpoint-list">
"""
    append_html(side_bar_before, stream)
    for ep in endpoints:
        path = ep["endpoint"]
        id = ep["id"]
        side_bar_content=f'<li><a style="padding:4px;" href="#{id}" class="active">{path}</a></li>'
        append_html(side_bar_content, stream)

    side_bar_after="""
            </ul>
        </aside>

        <main class="main-content">
    """
    append_html(side_bar_after, stream)

def append_endpoint_header(endpoint: endpoint, stream: File | None) -> None:
    method = endpoint["method"]
    path = endpoint["endpoint"]
    description = endpoint["description"]
    id = endpoint["id"]
    endpoint_path_template=f"""
            <section id="{id}" class="endpoint-section">
                <div class="endpoint-header">
                    <span class="method {method}">{method.upper()}</span>
                    <span class="endpoint-url">{path}</span>
                </div>
                
                <p class="endpoint-description">
                    {description}
                </p>
                    """
    append_html(endpoint_path_template, stream)

def append_parameters(parameters: list, stream: File | None) -> None:
    parameter_header="""
        
            <h3>Parameters</h3>
                <table class="parameter-table">
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            <th>Type</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                """
    append_html(parameter_header, stream)
    for parameter in parameters:
        name = parameter["name"]
        type = parameter["type"]
        required = parameter["required"]
        description = parameter["description"]
        parameter_template=f"""
                        <tr>
                            <td>{name}</td>
                            <td>{type}</td>
                            <td>{required}</td>
                            <td>{description}</td>
                        </tr>    """
        append_html(parameter_template, stream)

    parameter_footer="""
                    </tbody>
            </table>
     """
    append_html(parameter_footer, stream)
    pass

def append_request(request: str, id: str, stream: File | None) -> None:
    request_header=f"""
               <div class="tab-container">
                    <div class="tab-buttons">
                        <button class="tab-button active" onclick="openTab(event, 'request-{id}')">Request</button>
                        <button class="tab-button" onclick="openTab(event, 'response-{id}')">Response</button>
                    </div>
                    
                   <div class="tab-content">
                        <div id="request-{id}" class="tab-pane active">
                            <div class="code-block">
                                <pre>
                      """
    append_html(request_header, stream)
    for line in request:
        append_html(line, stream)
    request_footer=f"""
</pre>
                            </div>
                        </div>
 
    """
    append_html(request_footer, stream)
    pass    

def append_response(response: str, id: str, stream: File | None) -> None:
    response_header=f"""
                        <div id="response-{id}" class="tab-pane">
                            <div class="code-block">
                                <pre>
"""
    append_html(response_header, stream)
    for line in response:
        append_html(line, stream)
    response_footer="""                            </pre>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
    """
    append_html(response_footer, stream)
    
    pass

def main_loop(endpoints: list, stream: File | None) -> None:
    append_html(HTML_HEADER, stream)
    append_side_bar(endpoints, stream)
    for endpoint in endpoints:
        endpoint_path = endpoint['endpoint']
        id = endpoint["id"]
        description = endpoint['description']
        request = endpoint['request']
        response = endpoint['response']
        parameters = endpoint['parameters']
        append_endpoint_header(endpoint, stream)
        append_parameters(parameters, stream)
        append_request(request, id, stream)
        append_response(response, id, stream)
    append_html(HTML_FOOTER, stream)

if __name__ == "__main__":
    stream = None
    json_filenames = [file for file in os.listdir('.') if os.path.isfile(file) and file.endswith(".json")]
    endpoints = []
    for json_filename in json_filenames:
        with open(json_filename, "r") as json_file:
            endpoints += json.load(json_file)['endpoints']
    main_loop(endpoints, stream)
