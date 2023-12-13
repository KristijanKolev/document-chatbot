import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ChatSessionSimple} from "../../models/chatSessionSimple";
import {ChatService} from "../chat.service";

@Component({
  selector: 'app-sessions-overview',
  templateUrl: './sessions-overview.component.html',
  styleUrls: ['./sessions-overview.component.css']
})
export class SessionsOverviewComponent implements OnInit{
  @Output() onSessionSelect: EventEmitter<ChatSessionSimple> = new EventEmitter<ChatSessionSimple>();

  allSessions: ChatSessionSimple[] = [];
  selectedSession?: ChatSessionSimple;

  constructor(
    private chatService: ChatService
  ) { }

  ngOnInit(): void {
    this. loadAllSessions();
  }

  sessionClick(session: ChatSessionSimple) {
    this.selectedSession = session;
    this.onSessionSelect.emit(session)
  }

  createNewSession() {
    this.chatService.createChatSession().subscribe({
      next: _ => this.loadAllSessions(),
      error: err => console.error('Error creating new chat session. ', err),
    })
  }

  private loadAllSessions(): void {
    this.chatService.loadChatSessions().subscribe({
      next: sessions => this.allSessions = sessions,
      error: err => console.error('Error fetching chat sessions. ', err),
    });
  }
}
