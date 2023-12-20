import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, ReplaySubject, Subject} from "rxjs";
import {ChatSessionSimple} from "../models/chatSessionSimple";
import {ChatSession} from "../models/chatSession";
import {ChatPrompt} from "../models/chatPrompt";
import {SessionPromptingResponse} from "../models/sessionPromptingResponse"

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private _allSessions: ChatSessionSimple[] = [];
  public allSessions: Subject<ChatSessionSimple[]> = new ReplaySubject();

  constructor(
    private http: HttpClient
  ) { }

  public refreshChatSessions(): void {
      this.http.get<ChatSessionSimple[]>('/api/sessions').subscribe(
        sessions => {
          this._allSessions = sessions;
          this.allSessions.next(this._allSessions);
        }
      );
  }

  public loadChatSessionDetails(chatSessionID: number): Observable<ChatSession> {
    return this.http.get<ChatSession>(`/api/sessions/${chatSessionID}`);
  }

  public createPrompt(chatSessionID: number, promptText: string): Observable<SessionPromptingResponse> {
    const obsrv =  this.http.post<SessionPromptingResponse>(`/api/sessions/${chatSessionID}/prompt`, {'prompt': promptText});
    obsrv.subscribe(resp => {
      if (resp.session_updated) {
        this.refreshChatSessions();
      }
    });
    return obsrv;
  }

  public createChatSession(): Observable<ChatSession> {
    const obsrv = this.http.post<ChatSession>(`/api/sessions/`, {});
    obsrv.subscribe(
      newSession => {
        this._allSessions.push(newSession);
        this.allSessions.next(this._allSessions);
      }
    )
    return obsrv;
  }

  public renameChatSession(chatSessionID: number, name: string): Observable<ChatSession> {
    const obsrv = this.http.put<ChatSession>(`/api/sessions/${chatSessionID}`, {name: name});
    obsrv.subscribe(
      editedSession => {
        const idx = this._allSessions.findIndex(session => session.id == editedSession.id);
        this._allSessions[idx] = editedSession;
        this.allSessions.next(this._allSessions);
      }
    );
    return obsrv;
  }
}
