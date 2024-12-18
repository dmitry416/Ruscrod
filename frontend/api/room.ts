import apiClient from "../src/axios";
import type {AxiosInstance} from "axios";

const roomURL = 'rooms';

export function getRooms(): Promise<AxiosInstance> {
    return apiClient.get(`${roomURL}/get_rooms/`)
}

export function getRoomMessages(roomID: number, page: number): Promise<AxiosInstance> {
    return apiClient.get(`${roomURL}/${roomID}/get_room_messages/?page=${page}`)
}

export function getRoomMembers(roomID: number): Promise<AxiosInstance> {
    return apiClient.get(`${roomURL}/${roomID}/get_room_members/`)
}

export function createRoom(roomName: string, friendName: string): Promise<AxiosInstance> {
    return apiClient.post(`${roomURL}/create_room/`, {name: roomName, friend_name: friendName})
}

export function addFriendToRoom(roomID: number, friendName: string): Promise<AxiosInstance> {
    return apiClient.post(`${roomURL}/${roomID}/add_friend_to_room/`, {friend_name: friendName})
}