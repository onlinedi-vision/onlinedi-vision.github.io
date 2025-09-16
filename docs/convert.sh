#/usr/bin/env bash

read -p "New Endpoint: " endpoint
read -p "Endpoint Method (get/post/delete/...): " method 
read -p "Description: " desc

echo "Describe a curl call to the API endpoint (last line must be DONE):"

curl_call=""
while IFS= read -r line; do
  if [[ "$line" == "DONE" ]]; then
    break
  fi
  curl_call+="$line"$'\n'
done

cat > new.html <<EOF
                <div class="endpoint-header">
                    <span class="method ${method}">${method^^}</span>
                    <span class="endpoint-url">${endpoint}</span>
                </div>
                
                <p class="endpoint-description">
                     ${desc}
                </p>



                 <div class="tab-container">
                    <div class="tab-buttons">
                        <button class="tab-button active" onclick="openTab(event, 'request-users-get-all')">Request</button>
                        <button class="tab-button" onclick="openTab(event, 'response-users-get-all')">Response</button>
                    </div>
                    
                    <div class="tab-content">
                        <div id="request-users-get-all" class="tab-pane active">
                            <div class="code-block">
                                <pre>${curl_call}</pre>
                            </div>
                        </div>
                        
                        <div id="response-users-get-all" class="tab-pane">
                            <div class="code-block">
                                <pre>{
       "<span class="code-key">token</span>": <span class="code-number">asduh348yfhgasudifg...</span>,
}</pre>
                            </div>
                        </div>
                    </div>
                </div>
EOF

echo "This is the resulted HTML content: "
cat new.html
