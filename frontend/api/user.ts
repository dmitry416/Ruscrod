import apiClient from "../src/axios";

const userURL = 'users';

export function getFriends(): any {
    return apiClient.get(`${userURL}/get_friends/`)
}

export function addFriend(friendName: string): any {
    return apiClient.post(`${userURL}/add_friends/`, {name: friendName})
}

export function deleteFriend(friendName: string): any {
    return apiClient.post(`${userURL}/delete_friends/`, {name: friendName})
}