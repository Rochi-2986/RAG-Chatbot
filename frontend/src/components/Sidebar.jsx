import "./Sidebar.css";

function Sidebar({

    chats,
    activeChat,
    setActiveChat,
    newChat

}) {

    return (

        <div className="sidebar">

            <button
                className="new-chat-btn"
                onClick={newChat}
            >
                + New Chat
            </button>

            {

                chats.map(chat => (

                    <div

                        key={chat.id}

                        className={
                            activeChat === chat.id
                                ? "chat-item active"
                                : "chat-item"
                        }

                        onClick={() =>
                            setActiveChat(chat.id)
                        }

                    >

                        {chat.title}

                    </div>

                ))

            }

        </div>

    );

}

export default Sidebar;