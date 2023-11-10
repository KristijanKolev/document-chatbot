import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SessionsOverviewComponent } from './sessions-overview/sessions-overview.component';
import { ChatPage } from './chat-page/chat.page';
import { ChatBodyComponent } from './chat-body/chat-body.component';
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [
    SessionsOverviewComponent,
    ChatPage,
    ChatBodyComponent
  ],
  imports: [
    CommonModule,
    FormsModule
  ]
})
export class ChatModule { }
