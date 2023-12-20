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
    this.chatService.allSessions.subscribe(
      sessions => {
        this.allSessions = sessions;
        console.log('Sessions received!');
      }
    );
    this.chatService.refreshChatSessions();
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
    this.chatService.createChatSession();
  }

  startSessionEditing(session: ChatSessionSimple) {
    this.isSingleSessionNameClick = false;
    this.nameEditingSession = session;
    this.nameEditingInputValue = session.name;
  }

  finishSessionEditing(session: ChatSessionSimple) {
    this.chatService.renameChatSession(session.id, this.nameEditingInputValue);
    this.cancelSessionEditing();
  }

  cancelSessionEditing() {
    this.nameEditingSession = undefined;
    this.nameEditingInputValue = '';
  }
}
