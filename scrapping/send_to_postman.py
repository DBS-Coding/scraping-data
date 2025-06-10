import json
import requests
import time

# Load data from JSON file
def load_data():
    with open(r"c:\PythonVSCenv\Capstone\scrapping\output\content_by_author_and_tags.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def send_tag_to_api(tag_data, author_name):
    """Send single tag data to API"""
    url = "https://capstone-five-dusky.vercel.app/chatbot/tags"
    
    # Transform data sesuai struktur API
    payload = {
        "tag": tag_data["tag"],
        "nama": author_name,
        "input": tag_data["input"],
        "responses": tag_data["responses"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        print(f"🔄 Sending [{author_name}] Tag: {tag_data['tag']}")
        print(f"   URL: {url}")
        print(f"   Payload preview: tag='{tag_data['tag']}', nama='{author_name}', inputs={len(tag_data['input'])}, responses={len(tag_data['responses'])}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"   ✅ SUCCESS! [{author_name}] Tag: {tag_data['tag']}")
            try:
                response_data = response.json()
                if 'message' in response_data:
                    print(f"   📝 Message: {response_data['message']}")
            except:
                pass
            return True
        else:
            print(f"   ❌ FAILED! Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def get_all_tags_from_api():
    """Get all tags from API to see what's available"""
    url = "https://capstone-five-dusky.vercel.app/chatbot/tags"
    
    try:
        print("📋 Fetching all tags from API...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle different response structures
            if 'data' in data:
                tags = data['data']
            elif isinstance(data, list):
                tags = data
            else:
                tags = [data]
            
            print(f"✅ Found {len(tags)} tags in API")
            return tags
        else:
            print(f"❌ Failed to fetch tags: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching tags: {e}")
        return []

def delete_tag_from_api(tag_id=None, tag_name=None, author_name=None):
    """Delete tag from API"""
    # Multiple possible delete endpoints
    possible_endpoints = [
        f"https://capstone-five-dusky.vercel.app/chatbot/tags/{tag_id}" if tag_id else None,
        f"https://capstone-five-dusky.vercel.app/chatbot/tags/delete",
        f"https://capstone-five-dusky.vercel.app/chatbot/tags",
    ]
    
    # Filter out None values
    possible_endpoints = [url for url in possible_endpoints if url]
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Payload for delete (if needed)
    delete_payload = {}
    if tag_name and author_name:
        delete_payload = {
            "tag": tag_name,
            "nama": author_name
        }
    
    print(f"🗑️  Deleting tag: {tag_name} by {author_name}")
    
    for i, url in enumerate(possible_endpoints, 1):
        try:
            print(f"  Attempt {i}: {url}")
            
            # Try DELETE method first
            if tag_id and i == 1:
                response = requests.delete(url, headers=headers, timeout=10)
                print(f"    Method: DELETE")
            else:
                # Try POST with delete payload
                response = requests.post(url, json=delete_payload, headers=headers, timeout=10)
                print(f"    Method: POST with delete payload")
            
            print(f"    Response Status: {response.status_code}")
            
            if response.status_code in [200, 201, 204]:
                print(f"    ✅ SUCCESS! Deleted {tag_name}")
                return True
            else:
                print(f"    ❌ Failed: {response.status_code}")
                print(f"    Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    return False

def update_tag_in_api(tag_id=None, tag_name=None, author_name=None, updated_data=None):
    """Update tag in API (for removing specific inputs/responses)"""
    possible_endpoints = [
        f"https://capstone-five-dusky.vercel.app/chatbot/tags/{tag_id}" if tag_id else None,
        f"https://capstone-five-dusky.vercel.app/chatbot/tags/update",
        f"https://capstone-five-dusky.vercel.app/chatbot/tags",
    ]
    
    # Filter out None values
    possible_endpoints = [url for url in possible_endpoints if url]
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print(f"🔄 Updating tag: {tag_name} by {author_name}")
    
    for i, url in enumerate(possible_endpoints, 1):
        try:
            print(f"  Attempt {i}: {url}")
            
            # Try PUT method first, then POST
            if i == 1 and tag_id:
                response = requests.put(url, json=updated_data, headers=headers, timeout=10)
                print(f"    Method: PUT")
            else:
                response = requests.post(url, json=updated_data, headers=headers, timeout=10)
                print(f"    Method: POST")
            
            print(f"    Response Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"    ✅ SUCCESS! Updated {tag_name}")
                return True
            else:
                print(f"    ❌ Failed: {response.status_code}")
                print(f"    Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    return False

def delete_specific_tag():
    """Delete specific tag from API"""
    print("🗑️  DELETE SPECIFIC TAG FROM API")
    print("="*50)
    
    # Get tags from API
    api_tags = get_all_tags_from_api()
    
    if not api_tags:
        print("❌ No tags found in API or failed to fetch!")
        return
    
    # Display available tags
    print("\n📋 Available tags in API:")
    for i, tag in enumerate(api_tags, 1):
        tag_name = tag.get('tag', 'Unknown')
        author_name = tag.get('nama', 'Unknown')
        input_count = len(tag.get('input', []))
        response_count = len(tag.get('responses', []))
        print(f"{i}. {tag_name} by {author_name} ({input_count} inputs, {response_count} responses)")
    
    try:
        choice = int(input(f"\nPilih tag untuk dihapus (1-{len(api_tags)}): "))
        if 1 <= choice <= len(api_tags):
            selected_tag = api_tags[choice - 1]
            tag_name = selected_tag.get('tag', 'Unknown')
            author_name = selected_tag.get('nama', 'Unknown')
            tag_id = selected_tag.get('id')
            
            print(f"\n⚠️  You are about to delete:")
            print(f"   Tag: {tag_name}")
            print(f"   Author: {author_name}")
            print(f"   Inputs: {len(selected_tag.get('input', []))}")
            print(f"   Responses: {len(selected_tag.get('responses', []))}")
            if tag_id:
                print(f"   ID: {tag_id}")
            
            confirm = input("\nAre you sure? (y/n): ")
            if confirm.lower() == 'y':
                if delete_tag_from_api(tag_id, tag_name, author_name):
                    print("🎉 Tag deleted successfully!")
                else:
                    print("❌ Failed to delete tag!")
            else:
                print("❌ Deletion cancelled!")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_by_author():
    """Delete all tags from specific author"""
    print("🗑️  DELETE ALL TAGS BY AUTHOR")
    print("="*50)
    
    # Get tags from API
    api_tags = get_all_tags_from_api()
    
    if not api_tags:
        print("❌ No tags found in API!")
        return
    
    # Group by author
    authors = {}
    for tag in api_tags:
        author = tag.get('nama', 'Unknown')
        if author not in authors:
            authors[author] = []
        authors[author].append(tag)
    
    # Display authors
    print("\n📚 Available authors:")
    author_list = list(authors.keys())
    for i, author in enumerate(author_list, 1):
        tag_count = len(authors[author])
        print(f"{i}. {author} ({tag_count} tags)")
    
    try:
        choice = int(input(f"\nPilih author untuk dihapus semua tagnya (1-{len(author_list)}): "))
        if 1 <= choice <= len(author_list):
            selected_author = author_list[choice - 1]
            tags_to_delete = authors[selected_author]
            
            print(f"\n⚠️  You are about to delete {len(tags_to_delete)} tags from {selected_author}:")
            for tag in tags_to_delete:
                print(f"   - {tag.get('tag', 'Unknown')}")
            
            confirm = input(f"\nDelete all {len(tags_to_delete)} tags? (y/n): ")
            if confirm.lower() == 'y':
                success_count = 0
                for tag in tags_to_delete:
                    tag_name = tag.get('tag', 'Unknown')
                    tag_id = tag.get('id')
                    
                    if delete_tag_from_api(tag_id, tag_name, selected_author):
                        success_count += 1
                    
                    time.sleep(1)  # Delay between deletions
                
                print(f"\n✅ Deleted {success_count}/{len(tags_to_delete)} tags")
            else:
                print("❌ Deletion cancelled!")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_specific_inputs_responses():
    """Delete specific inputs or responses from a tag"""
    print("🗑️  DELETE SPECIFIC INPUTS/RESPONSES")
    print("="*50)
    
    # Get tags from API
    api_tags = get_all_tags_from_api()
    
    if not api_tags:
        print("❌ No tags found in API!")
        return
    
    # Display available tags
    print("\n📋 Available tags:")
    for i, tag in enumerate(api_tags, 1):
        tag_name = tag.get('tag', 'Unknown')
        author_name = tag.get('nama', 'Unknown')
        input_count = len(tag.get('input', []))
        response_count = len(tag.get('responses', []))
        print(f"{i}. {tag_name} by {author_name} ({input_count} inputs, {response_count} responses)")
    
    try:
        choice = int(input(f"\nPilih tag untuk diedit (1-{len(api_tags)}): "))
        if 1 <= choice <= len(api_tags):
            selected_tag = api_tags[choice - 1]
            edit_tag_inputs_responses(selected_tag)
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def edit_tag_inputs_responses(tag):
    """Edit inputs and responses of a specific tag"""
    tag_name = tag.get('tag', 'Unknown')
    author_name = tag.get('nama', 'Unknown')
    tag_id = tag.get('id')
    
    while True:
        print(f"\n" + "="*60)
        print(f"✏️  EDITING TAG: {tag_name} by {author_name}")
        print("="*60)
        
        current_inputs = tag.get('input', [])
        current_responses = tag.get('responses', [])
        
        print(f"📝 Current Inputs ({len(current_inputs)}):")
        for i, inp in enumerate(current_inputs, 1):
            print(f"  {i}. {inp}")
        
        print(f"\n💬 Current Responses ({len(current_responses)}):")
        for i, resp in enumerate(current_responses, 1):
            print(f"  {i}. {resp[:80]}{'...' if len(resp) > 80 else ''}")
        
        print("\n" + "="*60)
        print("PILIHAN:")
        print("1. Delete Specific Input")
        print("2. Delete Specific Response")
        print("3. Delete Multiple Inputs")
        print("4. Delete Multiple Responses")
        print("5. Save Changes to API")
        print("6. Back to Main Menu")
        
        choice = input("\nPilih aksi (1-6): ").strip()
        
        if choice == '1':
            delete_specific_input(tag)
        elif choice == '2':
            delete_specific_response(tag)
        elif choice == '3':
            delete_multiple_inputs(tag)
        elif choice == '4':
            delete_multiple_responses(tag)
        elif choice == '5':
            save_tag_changes(tag)
        elif choice == '6':
            break
        else:
            print("❌ Pilihan tidak valid!")

def delete_specific_input(tag):
    """Delete specific input from tag"""
    inputs = tag.get('input', [])
    
    if not inputs:
        print("❌ No inputs to delete!")
        return
    
    print("\n📝 Select input to delete:")
    for i, inp in enumerate(inputs, 1):
        print(f"{i}. {inp}")
    
    try:
        choice = int(input(f"\nPilih input untuk dihapus (1-{len(inputs)}): "))
        if 1 <= choice <= len(inputs):
            deleted_input = inputs.pop(choice - 1)
            print(f"✅ Deleted input: {deleted_input}")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_specific_response(tag):
    """Delete specific response from tag"""
    responses = tag.get('responses', [])
    
    if not responses:
        print("❌ No responses to delete!")
        return
    
    print("\n💬 Select response to delete:")
    for i, resp in enumerate(responses, 1):
        print(f"{i}. {resp[:100]}{'...' if len(resp) > 100 else ''}")
    
    try:
        choice = int(input(f"\nPilih response untuk dihapus (1-{len(responses)}): "))
        if 1 <= choice <= len(responses):
            deleted_response = responses.pop(choice - 1)
            print(f"✅ Deleted response: {deleted_response[:50]}...")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_multiple_inputs(tag):
    """Delete multiple inputs from tag"""
    inputs = tag.get('input', [])
    
    if not inputs:
        print("❌ No inputs to delete!")
        return
    
    print("\n📝 Select inputs to delete (comma-separated numbers):")
    for i, inp in enumerate(inputs, 1):
        print(f"{i}. {inp}")
    
    try:
        selections = input("\nEnter input numbers (e.g., 1,3,5): ").strip()
        if not selections:
            print("❌ No selection made!")
            return
        
        indices = [int(x.strip()) - 1 for x in selections.split(',')]
        indices.sort(reverse=True)  # Sort in reverse to avoid index issues
        
        deleted_count = 0
        for idx in indices:
            if 0 <= idx < len(inputs):
                deleted_input = inputs.pop(idx)
                deleted_count += 1
                print(f"✅ Deleted: {deleted_input}")
            else:
                print(f"⚠️  Invalid index: {idx + 1}")
        
        print(f"✅ Total deleted: {deleted_count} inputs")
        
    except ValueError:
        print("❌ Invalid input format!")

def delete_multiple_responses(tag):
    """Delete multiple responses from tag"""
    responses = tag.get('responses', [])
    
    if not responses:
        print("❌ No responses to delete!")
        return
    
    print("\n💬 Select responses to delete (comma-separated numbers):")
    for i, resp in enumerate(responses, 1):
        print(f"{i}. {resp[:80]}{'...' if len(resp) > 80 else ''}")
    
    try:
        selections = input("\nEnter response numbers (e.g., 1,3,5): ").strip()
        if not selections:
            print("❌ No selection made!")
            return
        
        indices = [int(x.strip()) - 1 for x in selections.split(',')]
        indices.sort(reverse=True)  # Sort in reverse to avoid index issues
        
        deleted_count = 0
        for idx in indices:
            if 0 <= idx < len(responses):
                deleted_response = responses.pop(idx)
                deleted_count += 1
                print(f"✅ Deleted: {deleted_response[:50]}...")
            else:
                print(f"⚠️  Invalid index: {idx + 1}")
        
        print(f"✅ Total deleted: {deleted_count} responses")
        
    except ValueError:
        print("❌ Invalid input format!")

def save_tag_changes(tag):
    """Save tag changes back to API"""
    tag_name = tag.get('tag', 'Unknown')
    author_name = tag.get('nama', 'Unknown')
    tag_id = tag.get('id')
    
    print(f"\n💾 Saving changes for tag: {tag_name}")
    print(f"   Inputs: {len(tag.get('input', []))}")
    print(f"   Responses: {len(tag.get('responses', []))}")
    
    confirm = input("\nSave changes to API? (y/n): ")
    if confirm.lower() == 'y':
        updated_data = {
            "tag": tag_name,
            "nama": author_name,
            "input": tag.get('input', []),
            "responses": tag.get('responses', [])
        }
        
        if update_tag_in_api(tag_id, tag_name, author_name, updated_data):
            print("🎉 Changes saved successfully!")
        else:
            print("❌ Failed to save changes!")
    else:
        print("❌ Changes not saved!")

def test_single_request():
    """Test dengan single request untuk debugging"""
    print("🧪 Testing single request...")
    print("="*50)
    
    data = load_data()
    
    # Ambil sample data pertama
    first_author = list(data.keys())[0]
    first_tag = data[first_author]['intents'][0]
    
    print(f"Testing dengan data:")
    print(f"Author: {first_author}")
    print(f"Tag: {first_tag['tag']}")
    print(f"Inputs: {len(first_tag['input'])}")
    print(f"Responses: {len(first_tag['responses'])}")
    print()
    
    # Show payload yang akan dikirim
    payload = {
        "tag": first_tag["tag"],
        "nama": first_author,
        "input": first_tag["input"],
        "responses": first_tag["responses"]
    }
    
    print("📤 Payload yang akan dikirim:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print()
    
    # Confirm before sending
    confirm = input("Lanjutkan test request? (y/n): ")
    if confirm.lower() == 'y':
        result = send_tag_to_api(first_tag, first_author)
        if result:
            print("🎉 Test request berhasil!")
        else:
            print("❌ Test request gagal!")
    else:
        print("Test dibatalkan.")

def push_all_data():
    """Push semua data ke API"""
    print("🚀 Starting data push to API...")
    print("="*60)
    
    data = load_data()
    
    total_tags = 0
    success_count = 0
    failed_count = 0
    
    # Count total tags
    for author, author_data in data.items():
        total_tags += len(author_data.get('intents', []))
    
    print(f"📊 Total tags to push: {total_tags}")
    print(f"🌐 Target URL: https://capstone-five-dusky.vercel.app/chatbot/tags")
    print("="*60)
    
    # Push data for each author
    for author, author_data in data.items():
        print(f"\n📤 Processing {author}...")
        intents = author_data.get('intents', [])
        
        for i, intent in enumerate(intents, 1):
            print(f"\n[{i}/{len(intents)}] Processing tag: {intent['tag']}")
            
            if send_tag_to_api(intent, author):
                success_count += 1
                print(f"   ✅ Success count: {success_count}")
            else:
                failed_count += 1
                print(f"   ❌ Failed count: {failed_count}")
            
            # Small delay to avoid overwhelming the API
            print(f"   ⏳ Waiting 2 seconds...")
            time.sleep(2)
    
    # Summary
    print("\n" + "="*60)
    print("📋 PUSH SUMMARY")
    print("="*60)
    print(f"✅ Successfully pushed: {success_count}/{total_tags}")
    print(f"❌ Failed: {failed_count}/{total_tags}")
    print(f"📊 Success rate: {(success_count/total_tags*100):.1f}%")
    
    if failed_count == 0:
        print("🎉 All data pushed successfully!")
    else:
        print(f"⚠️  {failed_count} tags failed to push. Check logs above.")

def push_by_author():
    """Push data berdasarkan author tertentu"""
    data = load_data()
    authors = list(data.keys())
    
    print("📚 Available authors:")
    for i, author in enumerate(authors, 1):
        tag_count = len(data[author].get('intents', []))
        print(f"{i}. {author} ({tag_count} tags)")
    
    try:
        choice = int(input(f"\nPilih author (1-{len(authors)}): "))
        if 1 <= choice <= len(authors):
            selected_author = authors[choice - 1]
            
            print(f"\n🚀 Pushing data for {selected_author}...")
            print(f"🌐 Target URL: https://capstone-five-dusky.vercel.app/chatbot/tags")
            print("="*50)
            
            intents = data[selected_author].get('intents', [])
            success_count = 0
            failed_count = 0
            
            for i, intent in enumerate(intents, 1):
                print(f"\n[{i}/{len(intents)}] Processing tag: {intent['tag']}")
                
                if send_tag_to_api(intent, selected_author):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Delay between requests
                if i < len(intents):
                    print(f"   ⏳ Waiting 2 seconds...")
                    time.sleep(2)
            
            print(f"\n" + "="*50)
            print(f"📋 SUMMARY FOR {selected_author}")
            print(f"✅ Successful: {success_count}/{len(intents)}")
            print(f"❌ Failed: {failed_count}/{len(intents)}")
            print(f"📊 Success rate: {(success_count/len(intents)*100):.1f}%")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def push_specific_tag():
    """Push tag tertentu"""
    data = load_data()
    
    # Select author
    authors = list(data.keys())
    print("📚 Available authors:")
    for i, author in enumerate(authors, 1):
        print(f"{i}. {author}")
    
    try:
        author_choice = int(input(f"\nPilih author (1-{len(authors)}): "))
        if 1 <= author_choice <= len(authors):
            selected_author = authors[author_choice - 1]
            
            # Select tag
            intents = data[selected_author].get('intents', [])
            print(f"\n🏷️  Available tags for {selected_author}:")
            for i, intent in enumerate(intents, 1):
                input_count = len(intent['input'])
                response_count = len(intent['responses'])
                print(f"{i}. {intent['tag']} ({input_count} inputs, {response_count} responses)")
            
            tag_choice = int(input(f"\nPilih tag (1-{len(intents)}): "))
            if 1 <= tag_choice <= len(intents):
                selected_tag = intents[tag_choice - 1]
                
                print(f"\n🚀 Pushing tag: {selected_tag['tag']} for {selected_author}")
                print(f"🌐 Target URL: https://capstone-five-dusky.vercel.app/chatbot/tags")
                print("-" * 50)
                
                if send_tag_to_api(selected_tag, selected_author):
                    print("\n🎉 Tag pushed successfully!")
                else:
                    print("\n❌ Failed to push tag!")
            else:
                print("❌ Invalid tag choice!")
        else:
            print("❌ Invalid author choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def check_data_preview():
    """Preview data yang akan dikirim"""
    data = load_data()
    
    print("📋 DATA PREVIEW")
    print("="*60)
    print("🌐 Target URL: https://capstone-five-dusky.vercel.app/chatbot/tags")
    print("="*60)
    
    for author, author_data in data.items():
        intents = author_data.get('intents', [])
        print(f"\n👤 {author} ({len(intents)} tags):")
        
        for i, intent in enumerate(intents, 1):
            print(f"\n   🏷️  {i}. {intent['tag']}")
            print(f"      📝 Inputs: {len(intent['input'])}")
            print(f"      💬 Responses: {len(intent['responses'])}")
            
            # Show structure that will be sent
            sample_payload = {
                "tag": intent["tag"],
                "nama": author,
                "input": intent["input"][:2] if len(intent["input"]) > 2 else intent["input"],
                "responses": intent["responses"][:1] if len(intent["responses"]) > 1 else intent["responses"]
            }
            
            print(f"      📤 API Payload structure:")
            print(f"         {{")
            print(f"           \"tag\": \"{sample_payload['tag']}\",")
            print(f"           \"nama\": \"{sample_payload['nama']}\",")
            print(f"           \"input\": {sample_payload['input']},")
            print(f"           \"responses\": {[r[:50] + '...' if len(r) > 50 else r for r in sample_payload['responses']]}")
            print(f"         }}")

def check_endpoint_connectivity():
    """Check if endpoint is reachable"""
    print("🔗 Checking endpoint connectivity...")
    print("="*50)
    
    url = "https://capstone-five-dusky.vercel.app/chatbot/tags"
    
    try:
        # Test GET request first
        print(f"Testing GET {url}")
        response = requests.get(url, timeout=10)
        print(f"GET Response: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print()
        
        # Test POST with minimal data
        print(f"Testing POST {url} with sample data")
        test_payload = {
            "tag": "test_connectivity",
            "nama": "Test",
            "input": ["test"],
            "responses": ["test response"]
        }
        
        response = requests.post(url, json=test_payload, timeout=10)
        print(f"POST Response: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code in [200, 201]:
            print("✅ Endpoint is working!")
        elif response.status_code == 404:
            print("❌ Endpoint not found (404)")
        elif response.status_code == 405:
            print("❌ Method not allowed (405)")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

def main_menu():
    """Main menu untuk push data"""
    while True:
        print("\n" + "="*60)
        print("🚀 CHATBOT TAGS MANAGER - API OPERATIONS")
        print("="*60)
        print("🌐 Target: https://capstone-five-dusky.vercel.app/chatbot/tags")
        print("="*60)
        print("📤 PUSH DATA:")
        print("1. Push All Data (Semua author & tag)")
        print("2. Push by Author (Pilih author tertentu)")
        print("3. Push Specific Tag (Pilih tag tertentu)")
        print()
        print("🔧 UTILITIES:")
        print("4. Preview Data (Lihat data yang akan dikirim)")
        print("5. Test Single Request (Debug)")
        print("6. Check Endpoint Connectivity")
        print("7. View All Tags in API")
        
        print("🗑️  DELETE/EDIT DATA:")
        print("8. Delete Specific Tag")
        print("9. Delete All Tags by Author")
        print("10. Delete/Edit Inputs & Responses")
        print("11. Exit")
        
        choice = input("\nPilih menu (1-11): ").strip()
        
        if choice == '1':
            confirm = input("⚠️  Push semua data? This will send ALL tags to API (y/n): ")
            if confirm.lower() == 'y':
                push_all_data()
            else:
                print("❌ Push dibatalkan!")
                
        elif choice == '2':
            push_by_author()
            
        elif choice == '3':
            push_specific_tag()
            
        elif choice == '4':
            check_data_preview()
            
        elif choice == '5':
            test_single_request()
            
        elif choice == '6':
            check_endpoint_connectivity()
            
        elif choice == '7':
            api_tags = get_all_tags_from_api()
            if api_tags:
                print(f"\n📋 Found {len(api_tags)} tags in API:")
                for i, tag in enumerate(api_tags, 1):
                    tag_name = tag.get('tag', 'Unknown')
                    author_name = tag.get('nama', 'Unknown')
                    input_count = len(tag.get('input', []))
                    response_count = len(tag.get('responses', []))
                    print(f"{i}. {tag_name} by {author_name} ({input_count} inputs, {response_count} responses)")
            
        elif choice == '8':
            delete_specific_tag()
            
        elif choice == '9':
            delete_by_author()
            
        elif choice == '10':
            delete_specific_inputs_responses()
            
        elif choice == '11':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")
        
        if choice in ['1', '2', '3', '5', '6', '7', '8', '9', '10']:
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()