import {HTTP_INTERCEPTORS, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {catchError, Observable, throwError} from "rxjs";
import {AuthenticationService} from "../authentication.service";
import {Router} from "@angular/router";
import {Injectable} from "@angular/core";

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(
    private authenticationService: AuthenticationService,
    private router: Router
  ) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(catchError(err => {
      if (err.status === 401) {
        console.log('Unauthorized');
        this.authenticationService.setToken(undefined);
        if(!this.router.url.includes('/login')) {
          this.router.navigate(['/login'], {
            queryParams: {
              return: this.router.url
            }
          }).then();
        }
      }

      throw err;
    }));
  }

}

export const authErrorInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
];
