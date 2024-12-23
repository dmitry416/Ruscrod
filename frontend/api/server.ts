import apiClient from "../src/axios";
import type {AxiosInstance} from "axios";

const serverURL = 'servers';

export function getServers(): Promise<AxiosInstance> {
    return apiClient.get(`${serverURL}/get_servers/`)
}

export function getServerRooms(serverID: number): Promise<AxiosInstance> {
    return apiClient.get(`${serverURL}/${serverID}/get_server_rooms/`)
}

export function getServerMembers(serverID: number): Promise<AxiosInstance> {
    return apiClient.get(`${serverURL}/${serverID}/get_server_members/`)
}

export function createServer(serverName: string, serverImage: File | null): Promise<AxiosInstance> {
    const formData = new FormData();
    formData.append('name', serverName);
    if (serverImage) {
        formData.append('image', serverImage);
    }
    return apiClient.post(`${serverURL}/create_server/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
}

export function setServerImage(serverID: number, serverImage: string): Promise<AxiosInstance> {
    return apiClient.post(`${serverURL}/${serverID}/set_server_image/`, {image: serverImage})
}

export function createServerRoom(serverID: number, serverRoomName: string): Promise<AxiosInstance> {
    return apiClient.post(`${serverURL}/${serverID}/create_server_room/`, {name: serverRoomName})
}

export function renameServerRoom(serverID: number, roomID: number, newName: string): Promise<AxiosInstance> {
    return apiClient.post(`${serverURL}/${serverID}/rename_server_room/`, {room_id: roomID, name: newName})
}

export function deleteServerRoom(serverID: number, roomID: number): Promise<AxiosInstance> {
    return apiClient.post(`${serverURL}/${serverID}/delete_server_room/`, {room_id: roomID})
}
