import {Component, OnInit} from '@angular/core';
import {CookieService} from "ngx-cookie-service";
import {AuthenticationService} from "./authentication/authentication.service";
import {User} from "./models/user";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'frontend';

  constructor(
    private cookieService: CookieService,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {
    if (this.cookieService.check('jwt')) {
      const token: string = this.cookieService.get('jwt');
      this.authenticationService.get_current_user_details(token).subscribe(
        (user: User) => {
          console.log(user);
        },
        (error) => {
          console.log(error);
        }
      )
    } else {
      console.log('JWT cookie missing!')
    }
  }


}
