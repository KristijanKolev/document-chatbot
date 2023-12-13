import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ChatSessionSimple} from "../models/chatSessionSimple";
import {ChatSession} from "../models/chatSession";
import {ChatPrompt} from "../models/chatPrompt";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(
    private http: HttpClient
  ) { }

  public loadChatSessions(): Observable<ChatSessionSimple[]> {
    return this.http.get<ChatSessionSimple[]>('/api/sessions');
  }

  public loadChatSessionDetails(chatSessionID: number): Observable<ChatSession> {
    return this.http.get<ChatSession>(`/api/sessions/${chatSessionID}`);
  }

  public createPrompt(chatSessionID: number, promptText: string): Observable<ChatPrompt> {
    return this.http.post<ChatPrompt>(`/api/sessions/${chatSessionID}/prompt`, {'prompt': promptText});
  }

  public createChatSession(): Observable<ChatSession> {
    return this.http.post<ChatSession>(`/api/sessions/`, {});
  }
}
