import apiClient from "../src/axios";

const roomURL = 'rooms';

export function getRooms(): any {
    return apiClient.get(`${roomURL}/get_rooms/`)
}

export function getRoomMessages(roomID: number, page: number): any {
    return apiClient.get(`${roomURL}/${roomID}/get_room_messages/?page=${page}`)
}

export function getRoomMembers(roomID: number): any {
    return apiClient.get(`${roomURL}/${roomID}/get_room_members/`)
}

export function createRoom(roomName: string, friendName: string): any {
    return apiClient.post(`${roomURL}/create_room/`, {name: roomName, friend_name: friendName})
}

export function addFriendToRoom(roomID: number, friendName: string): any {
    return apiClient.post(`${roomURL}/${roomID}/add_friend_to_room/`, {friend_name: friendName})
}