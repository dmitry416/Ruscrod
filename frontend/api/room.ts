import apiClient from "../src/axios";
import type {AxiosInstance} from "axios";

const roomURL = 'rooms';

export function getRooms(): Promise<AxiosInstance> {
    return apiClient.get(`${roomURL}/get_rooms/`)
}

export function getRoomMessages(roomID: number): Promise<AxiosInstance> {
    return apiClient.get(`${roomURL}/${roomID}/get_room_messages/`)
}

export function getRoomMembers(roomID: number): Promise<AxiosInstance> {
    return apiClient.get(`${roomURL}/${roomID}/get_room_members/`)
}

export function createRoom(roomName: string): Promise<AxiosInstance> {
    return apiClient.post(`${roomURL}/create_room/`, {name: roomName})
}

export function addFriendToRoom(roomID: number, friendName: string): Promise<AxiosInstance> {
    return apiClient.post(`${roomURL}/${roomID}/add_friend_to_room/`, {friend_name: friendName})
}

export function changeRoomName(roomID: number, newName: string): Promise<AxiosInstance> {
    return apiClient.post(`${roomURL}/${roomID}/change_room_name/`, {name: newName})
}

export function leaveFromRoom(roomID: number): Promise<AxiosInstance> {
    return apiClient.post(`${roomURL}/${roomID}/leave_from_room/`)
}