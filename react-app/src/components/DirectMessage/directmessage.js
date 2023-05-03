import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { io } from 'socket.io-client';
import { getDMS } from "../../store/messages";
let socket;

const Chat = () => {
    const [chatInput, setChatInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [isSending, setisSending]= useState(false)
    const user = useSelector(state => state.session.user)
    const dms = useSelector(state => state.messages)
    let messageList;
    if(dms){
        messageList = Object.values(dms)
    }
    const {userId, ownerId} = useParams()
    const dispatch = useDispatch()
    useEffect(() => {
        // open socket connection
        // create websocket
        socket = io();
        dispatch(getDMS(userId,ownerId))
        socket.on("chat", (chat) => {
            // Whenver a chat is sent, Dispatch our fetch to get all messages and set the messages to the returned list
            let msg = dispatch(getDMS(userId,ownerId))
            let msgArr = Object.values(msg)
            setMessages(...msgArr)
            console.log(messages)
        })
        // when component unmounts, disconnect
        return (() => {
            socket.disconnect()
        })
    }, [])

    const updateChatInput = (e) => {
        setChatInput(e.target.value)
    };
    // When we send a chat, we tell our socket in the backend what we're sending so that it can do work.
    const sendChat = (e) => {
        e.preventDefault()
        setisSending(true)
        socket.emit("chat", { user: user.username, msg: chatInput, recipient_id:ownerId, sender_id:userId });
        setisSending(false)
        setChatInput("")
    }

    return (user && (
        <div>
            <div>
                {dms && messageList.length > 0 && messageList.map((message, ind) => (
                    <div key={ind}>{`${message.sender.username}: ${message.msg}`}</div>
                ))}
            </div>
            <form onSubmit={sendChat}>
                <input
                    value={chatInput}
                    onChange={updateChatInput}
                />
                <button type="submit">Send</button>
            </form>
        </div>
    )
    )
};


export default Chat;
