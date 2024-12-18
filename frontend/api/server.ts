import apiClient from "../src/axios";

const serverURL = 'servers';

export function getServers(): any {
    return apiClient.get(`${serverURL}/get_servers/`)
}

export function getServerRooms(serverID: number): any {
    return apiClient.get(`${serverURL}/${serverID}/get_server_rooms/`)
}

export function getServerMembers(serverID: number): any {
    return apiClient.get(`${serverURL}/${serverID}/get_server_members/`)
}

export function createServer(serverName: string, serverImage: string): any {
    return apiClient.post(`${serverURL}/create_server/`, {name: serverName, image: serverImage})
}

export function setServerImage(serverID: number, serverImage: string): any {
    return apiClient.post(`${serverURL}/${serverID}/set_server_image/`, {image: serverImage})
}

export function creatServerRoom(roomID: number): any {
    return apiClient.post(`${serverURL}/${roomID}/delete_server_room/`)
}