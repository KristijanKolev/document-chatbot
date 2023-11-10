import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';
import {ChatSession} from "../../models/chatSession";

@Component({
  selector: 'app-chat-body',
  templateUrl: './chat-body.component.html',
  styleUrls: ['./chat-body.component.css']
})
export class ChatBodyComponent implements OnChanges {
  @Input() chatSession?: ChatSession;

  newPromptText: string = '';

  ngOnChanges(changes: SimpleChanges): void {
    let newSession = changes['chatSession'];

    console.log(this.chatSession);

    if (newSession) {
      this.newPromptText = '';
    }
  }
}
