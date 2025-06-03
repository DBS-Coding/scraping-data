import json
import requests
import time

# Load data from JSON file
def load_data():
    with open(r"c:\PythonVSCenv\Capstone\scrapping\content_by_author_and_tags.json", 'r', encoding='utf-8') as f:
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
        print("🚀 PUSH DATA TO API - CHATBOT TAGS")
        print("="*60)
        print("🌐 Target: https://capstone-five-dusky.vercel.app/chatbot/tags")
        print("="*60)
        print("1. Push All Data (Semua author & tag)")
        print("2. Push by Author (Pilih author tertentu)")
        print("3. Push Specific Tag (Pilih tag tertentu)")
        print("4. Preview Data (Lihat data yang akan dikirim)")
        print("5. Test Single Request (Debug)")
        print("6. Check Endpoint Connectivity")
        print("7. Exit")
        
        choice = input("\nPilih menu (1-7): ").strip()
        
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
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")
        
        if choice in ['1', '2', '3', '5', '6']:
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()