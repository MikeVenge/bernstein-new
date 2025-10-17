#!/usr/bin/env python3
"""
Script to upload PDF to Finchat and query each field from verification report.
This will populate a new column with PDF-extracted values.
"""

import csv
import os
import re
import time
from pathlib import Path

from adgolibs.finchat import FinchatClient
from adgolibs.consomme import ConsommeClient


# Keep backup manual client for reference
class FinchatAPIClientManual:
    """Simple Finchat API client using direct HTTP requests."""
    
    def __init__(self, base_url, api_token):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {api_token}',  # Use Token auth format
            'Content-Type': 'application/json'
        })
    
    def create_session(self, supplemental_prompt, consomme_token):
        """Create a Finchat session."""
        url = f"{self.base_url}/api/v1/sessions/"
        
        try:
            response = self.session.post(
                url,
                json={
                    "client_id": "bernstein_ipgp_analysis",  # Required field
                    "supplemental_prompt": supplemental_prompt,
                    "metadata": {"consomme_api_token": consomme_token}
                },
                timeout=300
            )
            response.raise_for_status()
            return response.json()
                    
        except Exception as e:
            raise Exception(f"Failed to create session: {str(e)}")
    
    def assign_documents(self, session_id, consomme_ids):
        """Assign documents to a session."""
        endpoints = [
            f"/api/v1/sessions/{session_id}/documents/",
            f"/v1/sessions/{session_id}/documents/",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json={"consomme_ids": consomme_ids},
                    timeout=300
                )
                if response.status_code in [200, 201]:
                    return response.json()
            except:
                continue
        return {}
    
    def get_session_status(self, session_id):
        """Get session status."""
        endpoints = [
            f"/api/v1/sessions/{session_id}/",
            f"/v1/sessions/{session_id}/",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(
                    f"{self.base_url}{endpoint}",
                    timeout=60
                )
                if response.status_code == 200:
                    return response.json()
            except:
                continue
        return {"status": "idle"}  # Assume idle if can't get status
    
    def wait_until_idle(self, session_id, max_wait=300):
        """Wait until session is idle (documents indexed)."""
        start = time.time()
        while time.time() - start < max_wait:
            status = self.get_session_status(session_id)
            if status.get('status') == 'idle':
                return True
            time.sleep(2)
        return False
    
    def send_message(self, session_id, message):
        """Send a message to the session."""
        endpoints = [
            f"/api/v1/sessions/{session_id}/chats/",
            f"/v1/sessions/{session_id}/chats/",
            f"/api/v1/sessions/{session_id}/messages/",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json={"message": message},
                    timeout=300
                )
                if response.status_code in [200, 201]:
                    return response.json()
            except:
                continue
        
        raise Exception("Failed to send message")
    
    def get_chat_response(self, session_id, chat_id, max_wait=60):
        """Wait for and get chat response."""
        start = time.time()
        
        endpoints = [
            f"/api/v1/sessions/{session_id}/chats/{chat_id}/",
            f"/v1/sessions/{session_id}/chats/{chat_id}",
            f"/v1/sessions/{session_id}/messages/{chat_id}/",
        ]
        
        while time.time() - start < max_wait:
            for endpoint in endpoints:
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        chat_data = response.json()
                        
                        # Check various status field names
                        status = chat_data.get('status') or chat_data.get('state')
                        if status in ['completed', 'done', 'ready']:
                            return chat_data
                        
                        # If we got a response but no status, return it anyway
                        if 'response' in chat_data or 'content' in chat_data:
                            return chat_data
                        
                except:
                    continue
            
            time.sleep(1)
        
        raise TimeoutError(f"Chat response timed out after {max_wait}s")


class ConsommeAPIClient:
    """Simple Consomme API client using direct HTTP requests."""
    
    def __init__(self, base_url, auth_token, app_name):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.app_name = app_name
        self.session = requests.Session()
    
    def upload_document(self, file_path):
        """Upload a document to Consomme."""
        # Try different endpoint paths
        endpoints_to_try = [
            "/api/v1/documents/",
            "/v1/documents/",
            "/documents/",
            "/upload/",
        ]
        
        last_error = None
        
        for endpoint in endpoints_to_try:
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': (file_path.name, f, 'application/pdf')}
                    
                    # Try different auth header formats
                    headers = {'Authorization': f'Bearer {self.auth_token}'}
                    data = {'app_name': self.app_name}
                    
                    url = f"{self.base_url}{endpoint}"
                    print(f"  Trying: {url}")
                    
                    response = requests.post(
                        url,
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=300
                    )
                    
                    if response.status_code == 200 or response.status_code == 201:
                        return response.json()
                    
                    last_error = f"{response.status_code}: {response.text[:100]}"
                    
            except Exception as e:
                last_error = str(e)
                continue
        
        # If all attempts failed, try with different auth format
        print(f"  Standard auth failed, trying token-based auth...")
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'application/pdf')}
                
                # Try token auth format
                data = {
                    'app_name': self.app_name,
                    'auth_token': self.auth_token
                }
                
                url = f"{self.base_url}/api/v1/documents/"
                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    timeout=300
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    return response.json()
                    
        except Exception as e:
            pass
        
        raise Exception(f"All upload attempts failed. Last error: {last_error}")


def upload_pdf_and_create_session():
    """Upload PDF to Consomme and create Finchat session using adgolibs."""
    
    # Get API credentials from environment variables
    consomme_url = os.environ.get("CONSOMME_API_URL")
    consomme_token = os.environ.get("CONSOMME_API_TOKEN")
    finchat_url = os.environ.get("FINCHAT_API_URL", os.environ.get("FINCHAT_URL", "https://finchat-api.adgo.dev"))
    finchat_token = os.environ.get("FINCHAT_API_TOKEN")
    
    if not all([consomme_url, consomme_token, finchat_token]):
        print("=" * 80)
        print("CONFIGURATION NEEDED")
        print("=" * 80)
        print("\nMissing environment variables. Please set:")
        print("\n  export CONSOMME_API_URL='...'")
        print("  export CONSOMME_API_TOKEN='...'")
        print("  export FINCHAT_API_TOKEN='...'")
        print("\n" + "=" * 80)
        return None, None
    
    print("=" * 80)
    print("STEP 1: UPLOADING PDF TO CONSOMME")
    print("=" * 80)
    
    # Initialize Consomme client using adgolibs
    consomme = ConsommeClient(
        base_url=consomme_url,
        auth_token=consomme_token,
        app_name="bernstein_analysis",
        timeout=300
    )
    
    # Upload PDF
    pdf_file = Path("2024Q2.pdf")
    if not pdf_file.exists():
        print(f"ERROR: PDF file '{pdf_file}' not found")
        return None, None
    
    print(f"Uploading {pdf_file}...")
    try:
        with open(pdf_file, 'rb') as f:
            result = consomme.upload_document(f, features={})
        
        consomme_doc_id = result["id"]
        print(f"✓ PDF uploaded successfully!")
        print(f"  Consomme Document ID: {consomme_doc_id}")
    except Exception as e:
        print(f"ERROR uploading to Consomme: {str(e)}")
        return None, None
    
    print("\n" + "=" * 80)
    print("STEP 2: CREATING FINCHAT SESSION")
    print("=" * 80)
    
    # Initialize Finchat client using adgolibs
    finchat = FinchatClient(
        base_url=finchat_url,
        api_token=finchat_token,
        debug=False,
        timeout=300
    )
    
    # Create session
    print("Creating Finchat session...")
    try:
        session_data = finchat.create_session(
            client_id="bernstein_ipgp_q2_2024",
            supplemental_prompt="You are a financial data extraction assistant. Extract exact numerical values from IPG Photonics Q2 2024 financial statements. Return ONLY the numerical value without explanation."
        )
        
        # Extract session ID from response
        session_id = session_data['id'] if isinstance(session_data, dict) else session_data
        
        print(f"✓ Session created: {session_id}")
        
        # Attach PDF to session
        print(f"Attaching PDF to session...")
        finchat.assign_documents_to_session(
            session_id=session_id,
            consomme_ids=[consomme_doc_id]
        )
        
        # Wait for indexing
        print("Waiting for document indexing...")
        finchat.wait_until_idle(session_id=session_id)
        print("✓ Document indexed and ready!")
        
        return finchat, session_id
        
    except Exception as e:
        print(f"ERROR creating Finchat session: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


def query_finchat(finchat, session_id, field_name, q1_value):
    """Query Finchat for a specific field value using adgolibs."""
    
    # Construct query
    query = f"What is the exact value for '{field_name}' in Q2 2024 (quarter ended June 30, 2024)? Return only the numerical value in thousands of dollars."
    
    try:
        # Send message using adgolibs method
        chat = finchat.send_chat_message(
            session_id=session_id,
            message=query
        )
        
        # Wait for response using adgolibs method
        response_data = finchat.wait_for_chat_response(
            session_id=session_id,
            previous_chat=chat
        )
        
        # Extract value from response
        # The response structure may have 'content', 'response', or 'answer'
        content = (response_data.get("content") or 
                   response_data.get("response") or 
                   response_data.get("answer") or "").strip()
        
        # Clean up the response
        # Remove common prefixes
        prefixes_to_remove = [
            "The value is ", "It is ", "The exact value is ", 
            "The value for", "For Q2 2024", "$", "USD", "The ", "is "
        ]
        
        for prefix in prefixes_to_remove:
            if content.lower().startswith(prefix.lower()):
                content = content[len(prefix):].strip()
        
        # Remove thousand separators and extra text
        cleaned = content.replace(",", "").strip()
        
        # Extract numerical value
        numbers = re.findall(r'-?\d+\.?\d*', cleaned)
        if numbers:
            return numbers[0]
        
        # Return as-is if we can't parse it
        return content if content else "NOT_FOUND"
            
    except Exception as e:
        print(f"ERROR: {str(e)[:80]}")
        return "ERROR"


def process_verification_report():
    """Process verification report and query Finchat for each field."""
    
    # Upload PDF and create session
    finchat, session_id = upload_pdf_and_create_session()
    
    if not finchat or not session_id:
        return
    
    print("\n" + "=" * 80)
    print("STEP 3: QUERYING FIELDS FROM PDF")
    print("=" * 80)
    
    # Read verification report
    verification_file = Path("verification_report.csv")
    if not verification_file.exists():
        print(f"ERROR: {verification_file} not found")
        return
    
    # Read all rows
    rows = []
    with open(verification_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Found {len(rows)} fields to query")
    print("\nQuerying Finchat (this may take a while)...\n")
    
    # Query each field
    results = []
    for i, row in enumerate(rows, 1):
        field_name = row['Target Field Name']
        q1_target = row['Q1 Target']
        
        print(f"[{i}/{len(rows)}] {field_name[:50]:50s} | Q1: {q1_target:>12s}", end=" | ")
        
        # Query Finchat
        pdf_value = query_finchat(finchat, session_id, field_name, q1_target)
        
        print(f"PDF: {pdf_value}")
        
        # Add PDF value to row
        row['Q2 PDF (Finchat)'] = pdf_value
        results.append(row)
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Save enhanced verification report
    output_file = Path("verification_report_with_pdf.csv")
    
    print("\n" + "=" * 80)
    print("STEP 4: SAVING RESULTS")
    print("=" * 80)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = list(rows[0].keys()) if rows else []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ Enhanced verification report saved: {output_file}")
    print(f"\nColumns:")
    print(f"  - Target Field Name")
    print(f"  - Source Sheet (from Excel)")
    print(f"  - Source Field Name (from Excel)")
    print(f"  - Q1 Target")
    print(f"  - Q1 Source")
    print(f"  - Q2 Target (Populated from Excel)")
    print(f"  - Match Status")
    print(f"  - Q2 PDF (Finchat) ← NEW!")
    
    # Summary statistics
    matched_count = sum(1 for r in results if r['Q2 PDF (Finchat)'] not in ['ERROR', ''])
    print(f"\n✓ Successfully queried {matched_count}/{len(results)} fields from PDF")


if __name__ == "__main__":
    try:
        process_verification_report()
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

