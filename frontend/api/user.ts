import apiClient from "../src/axios";
import type {AxiosInstance} from "axios";

const userURL = 'users';

export function getFriends(): Promise<AxiosInstance> {
    return apiClient.get(`${userURL}/get_friends/`);
}

export function addFriend(friendName: string): Promise<AxiosInstance> {
    return apiClient.post(`${userURL}/add_friend/`, {name: friendName});
}

export function deleteFriend(friendName: string): Promise<AxiosInstance> {
    return apiClient.post(`${userURL}/delete_friend/`, {name: friendName});
}