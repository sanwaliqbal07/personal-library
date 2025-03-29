import streamlit as st

# Initialize session state for storing books
if "library" not in st.session_state:
    st.session_state.library = []

# Set page config
st.set_page_config(page_title="Personal Library", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .stButton>button { width: 100%; border-radius: 8px; }
        .book-card {
            background: linear-gradient(to right, #ffdde1, #ee9ca7);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.15);
            margin-bottom: 10px;
            color: black;
            font-size: 16px;
        }
        .book-card h4 { margin: 0; font-size: 20px; font-weight: bold; }
        .book-card p { margin: 5px 0; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("📚 Personal Library Manager")

# Sidebar Menu
menu = st.sidebar.radio("📌 Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"])

# Add a Book
if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("📖 Book Title").strip()
        author = st.text_input("✍️ Author").strip()
    
    with col2:
        year = st.number_input("📅 Publication Year", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("🎭 Genre").strip()
    
    read_status = st.checkbox("✅ Have you read this book?")

    if st.button("Add Book", use_container_width=True):
        if title and author:
            new_book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
            st.session_state.library.append(new_book)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.warning("⚠️ Please enter both title and author!")

# Remove a Book
elif menu == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    if st.session_state.library:
        book_titles = [book["title"] for book in st.session_state.library]
        book_to_remove = st.selectbox("📖 Select a book to remove", book_titles)
        
        if st.button("Remove Book", use_container_width=True):
            st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
            st.success(f"✅ '{book_to_remove}' removed successfully!")
    else:
        st.warning("⚠️ No books available to remove!")

# **🔥 Fixed Search for a Book**
elif menu == "Search for a Book":
    st.subheader("🔍 Search for a Book")
    search_term = st.text_input("🔎 Enter book title or author").strip().lower()

    if st.button("Search", use_container_width=True):
        results = [
            book for book in st.session_state.library
            if search_term in book["title"].lower() or search_term in book["author"].lower()
        ]

        if results:
            st.success(f"✅ Found {len(results)} result(s)")
            for book in results:
                st.markdown(f"""
                <div class='book-card'>
                    <h4>📖 {book['title']}</h4>
                    <p>✍️ <b>{book['author']}</b> ({book['year']})</p>
                    <p>🎭 {book['genre']}</p>
                    <p>📖 {"✅ Read" if book['read'] else "❌ Unread"}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No matching books found!")

# **🔥 Improved Display All Books**
elif menu == "Display All Books":
    st.subheader("📚 Your Library")
    if st.session_state.library:
        num_books = len(st.session_state.library)
        cols = st.columns(3)  # 3 books per row

        for index, book in enumerate(st.session_state.library):
            with cols[index % 3]:  # Distribute books across columns
                st.markdown(f"""
                <div class='book-card'>
                    <h4>📖 {book['title']}</h4>
                    <p>✍️ <b>{book['author']}</b> ({book['year']})</p>
                    <p>🎭 {book['genre']}</p>
                    <p>📖 {"✅ Read" if book['read'] else "❌ Unread"}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Your library is empty!")

# Display Statistics
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books else 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📚 Total Books", total_books)
    with col2:
        st.metric("✅ Books Read", f"{read_books} ({percentage_read:.1f}%)")

    st.progress(percentage_read / 100)
    