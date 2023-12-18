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
  nameEditingSession?: ChatSessionSimple; // Will be set when a user clicks to edit the name of a session.
  nameEditingInputValue: string = '';

  private isSingleSessionNameClick: boolean = false;

  constructor(
    private chatService: ChatService
  ) { }

  ngOnInit(): void {
    this. loadAllSessions();
  }

  sessionClick(session: ChatSessionSimple) {
    if (!this.isSingleSessionNameClick) {
      this.isSingleSessionNameClick = true;
      setTimeout(() => {
        if (this.isSingleSessionNameClick) {
          this.selectedSession = session;
          this.onSessionSelect.emit(session);
          this.isSingleSessionNameClick = false;
        }
      }, 250);
    }
  }

  createNewSession() {
    this.chatService.createChatSession().subscribe({
      next: _ => this.loadAllSessions(),
      error: err => console.error('Error creating new chat session. ', err),
    })
  }

  startSessionEditing(session: ChatSessionSimple) {
    this.isSingleSessionNameClick = false;
    this.nameEditingSession = session;
    this.nameEditingInputValue = session.name;
  }

  finishSessionEditing(session: ChatSessionSimple) {
    this.chatService.renameChatSession(session.id, this.nameEditingInputValue).subscribe({
      next: _ => {
        this.loadAllSessions();
      },
      error: err => {
        console.error('Error renaming chat session. ', err);
        this.loadAllSessions();
      },
    });
    this.cancelSessionEditing();
  }

  cancelSessionEditing() {
    this.nameEditingSession = undefined;
    this.nameEditingInputValue = '';
  }

  private loadAllSessions() {
    this.chatService.loadChatSessions().subscribe({
      next: sessions => this.allSessions = sessions,
      error: err => console.error('Error fetching chat sessions. ', err),
    });
  }
}
