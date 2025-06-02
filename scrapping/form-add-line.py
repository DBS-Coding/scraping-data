import json
import os

# Path to JSON file
base_path = r"c:\PythonVSCenv\Capstone\scrapping"
json_file = os.path.join(base_path, "content_by_author_and_tags.json")

def load_data():
    """Load data from JSON file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ File tidak ditemukan!")
        return {}

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("✅ Data berhasil disimpan!")
        return True
    except Exception as e:
        print(f"❌ Error saat menyimpan: {e}")
        return False

def display_authors(data):
    """Display available authors"""
    authors = list(data.keys())
    print("\n📚 Authors yang tersedia:")
    for i, author in enumerate(authors, 1):
        print(f"{i}. {author}")
    return authors

def display_tags(author_data):
    """Display tags for selected author"""
    intents = author_data.get("intents", [])
    print(f"\n🏷️  Tags yang tersedia:")
    for i, intent in enumerate(intents, 1):
        print(f"{i}. {intent['tag']}")
    return intents

def select_author(data):
    """Select author from available options"""
    authors = display_authors(data)
    if not authors:
        print("❌ Tidak ada author yang tersedia!")
        return None
    
    while True:
        try:
            choice = int(input(f"\nPilih author (1-{len(authors)}): "))
            if 1 <= choice <= len(authors):
                return authors[choice - 1]
            else:
                print("❌ Pilihan tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

def add_tag(data):
    """Add new tag to selected author"""
    print("\n" + "="*50)
    print("🆕 MENAMBAH TAG BARU")
    print("="*50)
    
    author = select_author(data)
    if not author:
        return
    
    tag_name = input("\nMasukkan nama tag baru: ").strip()
    if not tag_name:
        print("❌ Nama tag tidak boleh kosong!")
        return
    
    # Check if tag already exists
    existing_tags = [intent['tag'] for intent in data[author].get('intents', [])]
    if tag_name in existing_tags:
        print(f"❌ Tag '{tag_name}' sudah ada!")
        return
    
    # Create new tag
    new_tag = {
        "tag": tag_name,
        "input": [],
        "responses": []
    }
    
    # Add inputs
    print(f"\n📝 Menambah input untuk tag '{tag_name}':")
    print("(Ketik 'done' untuk selesai)")
    while True:
        inp = input("Input: ").strip()
        if inp.lower() == 'done':
            break
        if inp:
            new_tag["input"].append(inp)
    
    # Add responses
    print(f"\n💬 Menambah responses untuk tag '{tag_name}':")
    print("(Ketik 'done' untuk selesai)")
    while True:
        resp = input("Response: ").strip()
        if resp.lower() == 'done':
            break
        if resp:
            new_tag["responses"].append(resp)
    
    # Add to data
    if 'intents' not in data[author]:
        data[author]['intents'] = []
    
    data[author]['intents'].append(new_tag)
    
    if save_data(data):
        print(f"✅ Tag '{tag_name}' berhasil ditambahkan untuk {author}!")

def delete_tag(data):
    """Delete tag from selected author"""
    print("\n" + "="*50)
    print("🗑️  MENGHAPUS TAG")
    print("="*50)
    
    author = select_author(data)
    if not author:
        return
    
    intents = display_tags(data[author])
    if not intents:
        print("❌ Tidak ada tag yang tersedia!")
        return
    
    while True:
        try:
            choice = int(input(f"\nPilih tag yang akan dihapus (1-{len(intents)}): "))
            if 1 <= choice <= len(intents):
                tag_to_delete = intents[choice - 1]
                confirm = input(f"⚠️  Yakin ingin menghapus tag '{tag_to_delete['tag']}'? (y/n): ")
                if confirm.lower() == 'y':
                    data[author]['intents'].remove(tag_to_delete)
                    if save_data(data):
                        print(f"✅ Tag '{tag_to_delete['tag']}' berhasil dihapus!")
                else:
                    print("❌ Penghapusan dibatalkan!")
                break
            else:
                print("❌ Pilihan tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

def edit_tag(data):
    """Edit existing tag"""
    print("\n" + "="*50)
    print("✏️  MENGEDIT TAG")
    print("="*50)
    
    author = select_author(data)
    if not author:
        return
    
    intents = display_tags(data[author])
    if not intents:
        print("❌ Tidak ada tag yang tersedia!")
        return
    
    while True:
        try:
            choice = int(input(f"\nPilih tag yang akan diedit (1-{len(intents)}): "))
            if 1 <= choice <= len(intents):
                edit_tag_menu(data, author, intents[choice - 1])
                break
            else:
                print("❌ Pilihan tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

def edit_tag_menu(data, author, selected_tag):
    """Edit tag submenu"""
    while True:
        print(f"\n" + "="*50)
        print(f"✏️  EDITING TAG: {selected_tag['tag']}")
        print("="*50)
        print("1. Add Input")
        print("2. Add Response")
        print("3. Delete Input")
        print("4. Delete Response")
        print("5. View Current Data")
        print("6. Audit Responses > 150 characters")
        print("7. Back to Main Menu")
        
        choice = input("\nPilih aksi (1-6): ").strip()
        
        if choice == '1':
            add_input_to_tag(data, author, selected_tag)
        elif choice == '2':
            add_response_to_tag(data, author, selected_tag)
        elif choice == '3':
            delete_input_from_tag(data, author, selected_tag)
        elif choice == '4':
            delete_response_from_tag(data, author, selected_tag)
        elif choice == '5':
            view_tag_data(selected_tag)
        elif choice == '6':
            audit_responses(data, author, selected_tag)
        elif choice == '7':
            break
        else:
            print("❌ Pilihan tidak valid!")

def audit_responses(data, author, tag):
    """Audit responses yang melebihi 150 karakter"""
    print(f"\n" + "="*50)
    print(f"🔍 AUDIT RESPONSES - TAG: {tag['tag']} [{author}]")
    print("="*50)
    
    responses = tag.get('responses', [])
    long_responses = []
    
    # Find responses longer than 150 characters
    for i, resp in enumerate(responses):
        if len(resp) > 150:
            long_responses.append({
                'index': i,
                'text': resp,
                'length': len(resp)
            })
    
    if not long_responses:
        print("✅ Tidak ada response yang melebihi 150 karakter!")
        return
    
    print(f"⚠️  Ditemukan {len(long_responses)} response yang melebihi 150 karakter:")
    print("-" * 50)
    
    for i, resp_data in enumerate(long_responses, 1):
        print(f"\n{i}. Response Index: {resp_data['index'] + 1}")
        print(f"   Panjang: {resp_data['length']} karakter")
        print(f"   Preview: {resp_data['text'][:100]}...")
    
    print("\n" + "="*50)
    print("PILIHAN TINDAKAN:")
    print("1. Edit Response Tertentu")
    print("2. Edit Semua Response Panjang")
    print("3. Kembali")
    
    choice = input("\nPilih tindakan (1-3): ").strip()
    
    if choice == '1':
        edit_specific_long_response(data, author, tag, long_responses)
    elif choice == '2':
        edit_all_long_responses(data, author, tag, long_responses)
    elif choice == '3':
        return
    else:
        print("❌ Pilihan tidak valid!")

def edit_specific_long_response(data, author, tag, long_responses):
    """Edit response tertentu yang panjang"""
    print(f"\n📝 EDIT RESPONSE TERTENTU")
    print("-" * 30)
    
    for i, resp_data in enumerate(long_responses, 1):
        print(f"{i}. Response {resp_data['index'] + 1} ({resp_data['length']} karakter)")
        print(f"   {resp_data['text'][:80]}...")
    
    while True:
        try:
            choice = int(input(f"\nPilih response yang akan diedit (1-{len(long_responses)}): "))
            if 1 <= choice <= len(long_responses):
                selected_resp = long_responses[choice - 1]
                edit_single_response(data, author, tag, selected_resp)
                break
            else:
                print("❌ Pilihan tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

def edit_all_long_responses(data, author, tag, long_responses):
    """Edit semua response yang panjang secara berurutan"""
    print(f"\n📝 EDIT SEMUA RESPONSE PANJANG")
    print("-" * 30)
    print(f"Total response yang akan diedit: {len(long_responses)}")
    
    confirm = input("\nLanjutkan mengedit semua response? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Edit dibatalkan!")
        return
    
    edited_count = 0
    for i, resp_data in enumerate(long_responses, 1):
        print(f"\n{'='*50}")
        print(f"📝 EDITING RESPONSE {i}/{len(long_responses)}")
        print(f"Response Index: {resp_data['index'] + 1}")
        print(f"Panjang: {resp_data['length']} karakter")
        print("="*50)
        
        if edit_single_response(data, author, tag, resp_data):
            edited_count += 1
        
        if i < len(long_responses):
            continue_edit = input(f"\nLanjutkan ke response berikutnya? (y/n): ")
            if continue_edit.lower() != 'y':
                break
    
    print(f"\n✅ Selesai! {edited_count} response berhasil diedit dari {len(long_responses)} response.")

def edit_single_response(data, author, tag, resp_data):
    """Edit single response"""
    original_text = resp_data['text']
    original_index = resp_data['index']
    
    print(f"\n📄 RESPONSE ASLI ({len(original_text)} karakter):")
    print("-" * 50)
    print(original_text)
    print("-" * 50)
    
    print("\nPILIHAN:")
    print("1. Tulis ulang response")
    print("2. Edit sebagian")
    print("3. Skip response ini")
    
    choice = input("\nPilih aksi (1-3): ").strip()
    
    if choice == '1':
        return rewrite_response(data, author, tag, original_index, original_text)
    elif choice == '2':
        return edit_partial_response(data, author, tag, original_index, original_text)
    elif choice == '3':
        print("⏭️  Response dilewati")
        return False
    else:
        print("❌ Pilihan tidak valid!")
        return False

def rewrite_response(data, author, tag, index, original_text):
    """Tulis ulang response dari awal"""
    print(f"\n✏️  MENULIS ULANG RESPONSE")
    print("💡 Tips: Usahakan tidak lebih dari 150 karakter")
    print("💡 Tekan Enter 2x jika ingin baris baru, atau ketik 'done' untuk selesai")
    print("-" * 50)
    
    new_text = ""
    line_count = 0
    
    while True:
        if line_count == 0:
            line = input("Response baru: ").strip()
        else:
            line = input("           : ").strip()
        
        if line.lower() == 'done':
            break
        
        if line == "" and line_count > 0:
            # Double enter to finish
            break
        
        if new_text:
            new_text += " " + line
        else:
            new_text = line
        
        line_count += 1
        
        # Show current length
        print(f"   📏 Panjang saat ini: {len(new_text)} karakter")
        
        if len(new_text) > 150:
            print(f"   ⚠️  Melebihi 150 karakter!")
    
    if not new_text:
        print("❌ Response kosong! Tidak ada perubahan.")
        return False
    
    # Confirm changes
    print(f"\n📋 PREVIEW PERUBAHAN:")
    print(f"Panjang baru: {len(new_text)} karakter")
    print(f"Response baru: {new_text}")
    
    confirm = input(f"\nSimpan perubahan? (y/n): ")
    if confirm.lower() == 'y':
        tag['responses'][index] = new_text
        if save_data(data):
            print(f"✅ Response berhasil diupdate!")
            return True
    else:
        print("❌ Perubahan dibatalkan!")
    
    return False

def edit_partial_response(data, author, tag, index, original_text):
    """Edit sebagian response"""
    print(f"\n✂️  EDIT SEBAGIAN RESPONSE")
    print("💡 Anda bisa memotong atau memperbaiki bagian tertentu")
    print("-" * 50)
    print(f"Original: {original_text}")
    print("-" * 50)
    
    print("\nResponse saat ini akan dimasukkan ke editor:")
    print("(Edit sesuai kebutuhan, ketik 'cancel' untuk membatalkan)")
    
    # Show current text for editing
    edited_text = input(f"Edit: {original_text}\n      ")
    
    if edited_text.lower() == 'cancel':
        print("❌ Edit dibatalkan!")
        return False
    
    if not edited_text.strip():
        print("❌ Response tidak boleh kosong!")
        return False
    
    # Show changes
    print(f"\n📋 PREVIEW PERUBAHAN:")
    print(f"Sebelum ({len(original_text)} karakter): {original_text}")
    print(f"Sesudah ({len(edited_text)} karakter): {edited_text}")
    
    if len(edited_text) > 150:
        print(f"⚠️  Masih melebihi 150 karakter!")
    else:
        print(f"✅ Sudah di bawah 150 karakter!")
    
    confirm = input(f"\nSimpan perubahan? (y/n): ")
    if confirm.lower() == 'y':
        tag['responses'][index] = edited_text
        if save_data(data):
            print(f"✅ Response berhasil diupdate!")
            return True
    else:
        print("❌ Perubahan dibatalkan!")
    
    return False

def add_input_to_tag(data, author, tag):
    """Add input to existing tag"""
    print(f"\n📝 Menambah input untuk tag '{tag['tag']}':")
    print("(Ketik 'done' untuk selesai)")
    
    added_count = 0
    while True:
        inp = input("Input baru: ").strip()
        if inp.lower() == 'done':
            break
        if inp:
            if inp not in tag["input"]:
                tag["input"].append(inp)
                added_count += 1
                print(f"✅ Input '{inp}' ditambahkan!")
            else:
                print(f"⚠️  Input '{inp}' sudah ada!")
    
    if added_count > 0:
        if save_data(data):
            print(f"✅ {added_count} input baru berhasil ditambahkan!")

def add_response_to_tag(data, author, tag):
    """Add response to existing tag"""
    print(f"\n💬 Menambah response untuk tag '{tag['tag']}':")
    print("(Ketik 'done' untuk selesai)")
    
    added_count = 0
    while True:
        resp = input("Response baru: ").strip()
        if resp.lower() == 'done':
            break
        if resp:
            if resp not in tag["responses"]:
                tag["responses"].append(resp)
                added_count += 1
                print(f"✅ Response '{resp[:50]}...' ditambahkan!")
            else:
                print(f"⚠️  Response sudah ada!")
    
    if added_count > 0:
        if save_data(data):
            print(f"✅ {added_count} response baru berhasil ditambahkan!")

def delete_input_from_tag(data, author, tag):
    """Delete input from tag"""
    if not tag["input"]:
        print("❌ Tidak ada input untuk dihapus!")
        return
    
    print(f"\n📝 Input untuk tag '{tag['tag']}':")
    for i, inp in enumerate(tag["input"], 1):
        print(f"{i}. {inp}")
    
    while True:
        try:
            choice = int(input(f"\nPilih input yang akan dihapus (1-{len(tag['input'])}): "))
            if 1 <= choice <= len(tag["input"]):
                deleted_input = tag["input"].pop(choice - 1)
                if save_data(data):
                    print(f"✅ Input '{deleted_input}' berhasil dihapus!")
                break
            else:
                print("❌ Pilihan tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

def delete_response_from_tag(data, author, tag):
    """Delete response from tag"""
    if not tag["responses"]:
        print("❌ Tidak ada response untuk dihapus!")
        return
    
    print(f"\n💬 Responses untuk tag '{tag['tag']}':")
    for i, resp in enumerate(tag["responses"], 1):
        print(f"{i}. {resp[:100]}...")
    
    while True:
        try:
            choice = int(input(f"\nPilih response yang akan dihapus (1-{len(tag['responses'])}): "))
            if 1 <= choice <= len(tag["responses"]):
                deleted_response = tag["responses"].pop(choice - 1)
                if save_data(data):
                    print(f"✅ Response berhasil dihapus!")
                break
            else:
                print("❌ Pilihan tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

def view_tag_data(tag):
    """View current tag data"""
    print(f"\n" + "="*50)
    print(f"📊 DATA TAG: {tag['tag']}")
    print("="*50)
    
    print(f"\n📝 Inputs ({len(tag['input'])}):")
    for i, inp in enumerate(tag['input'], 1):
        print(f"  {i}. {inp}")
    
    print(f"\n💬 Responses ({len(tag['responses'])}):")
    for i, resp in enumerate(tag['responses'], 1):
        print(f"  {i}. {resp[:100]}{'...' if len(resp) > 100 else ''}")

def main_menu():
    """Main application menu"""
    print("\n" + "="*50)
    print("🏷️  CHATBOT TAG MANAGER")
    print("="*50)
    print("1. Add a Tag")
    print("2. Delete a Tag")
    print("3. Edit Tag")
    print("4. View All Data")
    print("5. Exit")

def view_all_data(data):
    """View all data in the JSON"""
    print("\n" + "="*50)
    print("📊 SEMUA DATA")
    print("="*50)
    
    for author, author_data in data.items():
        print(f"\n👤 {author}:")
        intents = author_data.get('intents', [])
        print(f"   Total tags: {len(intents)}")
        for intent in intents:
            print(f"   - {intent['tag']} ({len(intent['input'])} inputs, {len(intent['responses'])} responses)")

def main():
    """Main application loop"""
    print("🎯 Selamat datang di Chatbot Tag Manager!")
    
    while True:
        data = load_data()
        if not data:
            print("❌ Tidak dapat memuat data!")
            break
        
        main_menu()
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == '1':
            add_tag(data)
        elif choice == '2':
            delete_tag(data)
        elif choice == '3':
            edit_tag(data)
        elif choice == '4':
            view_all_data(data)
        elif choice == '5':
            print("👋 Terima kasih telah menggunakan Tag Manager!")
            break
        else:
            print("❌ Pilihan tidak valid!")
        
        input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()