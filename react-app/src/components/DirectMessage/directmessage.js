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
            let test = dispatch(getDMS(userId,ownerId))
            let testArry = Object.values(test)
            setMessages(...testArry)
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

    const sendChat = (e) => {
        e.preventDefault()
        setisSending(true)
        socket.emit("chat", { user: user.username, msg: chatInput, recipient_id:ownerId, sender_id:userId });
        setisSending(false)
        setChatInput("")
    }
    // useEffect(() => {
    //     dispatch(getDMS(userId,ownerId))

    // },[])
    console.log(messageList)
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
