import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {User} from "../models/user";
import {Observable} from "rxjs";
import {Token} from "../models/token";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private MILLIS_TO_MINUTES = 1000 * 60
  private REFRESH_INTERVAL: number = environment.JWT_EXPIRATION_DELTA * this.MILLIS_TO_MINUTES;
  private tokenRefreshTimeoutID: number = -1;


  public token?: string = undefined;

  constructor(
    private http: HttpClient
  ) { }

  public getCurrentUser(token: string): Observable<User> {
    const headers: HttpHeaders = new HttpHeaders({
      Authorization: `Bearer ${token}`
    })
    return this.http.get<User>('/api/users/me', {headers: headers})
  }

  setToken(token?: string) {
    this.token = token;
    if(token) {
      this.tokenRefreshTimeoutID = setTimeout(() => this.refreshToken(), this.REFRESH_INTERVAL);
    } else if (this.tokenRefreshTimeoutID >= 0) {
      clearInterval(this.tokenRefreshTimeoutID);
      this.tokenRefreshTimeoutID = -1;
    }
  }

  private refreshToken() {
    this.http.get<Token>('api/auth/refresh-token').subscribe(
      token => this.setToken(token.access_token)
    )
  }
}
