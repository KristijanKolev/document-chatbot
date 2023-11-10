import {Component, EventEmitter, Input, Output} from '@angular/core';
import {ChatSessionSimple} from "../../models/chatSessionSimple";

@Component({
  selector: 'app-sessions-overview',
  templateUrl: './sessions-overview.component.html',
  styleUrls: ['./sessions-overview.component.css']
})
export class SessionsOverviewComponent {
  @Input() chatSessions: ChatSessionSimple[] = [];
  @Output() onSessionSelect: EventEmitter<ChatSessionSimple> = new EventEmitter<ChatSessionSimple>();

  selectedSession?: ChatSessionSimple;

  sessionClick(session: ChatSessionSimple) {
    this.selectedSession = session;
    this.onSessionSelect.emit(session)
  }
}
