import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ChatSessionSimple} from "../models/chatSessionSimple";
import {ChatSession} from "../models/chatSession";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(
    private http: HttpClient
  ) { }

  public loadChatSessions(): Observable<ChatSessionSimple[]> {
    return this.http.get<ChatSessionSimple[]>('/api/sessions')
  }

  public loadChatSessionDetails(chatSessionID: number): Observable<ChatSession> {
    return this.http.get<ChatSession>(`/api/sessions/${chatSessionID}`);
  }
}
