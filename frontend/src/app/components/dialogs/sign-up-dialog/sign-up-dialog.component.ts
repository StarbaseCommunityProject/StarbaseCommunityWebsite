import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../../../services/authentication/authentication.service';
import { PasswordErrorStateMatcher, passwordValidator } from '../../validators/authentication.validators';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-sign-up-dialog',
  templateUrl: './sign-up-dialog.component.html',
  styleUrls: ['./sign-up-dialog.component.scss']
})
export class SignUpDialogComponent implements OnInit {

  signUpForm: FormGroup;
  logInForm: FormGroup;
  passwordErrorStateMatcher = new PasswordErrorStateMatcher()

  constructor( private formBuilder: FormBuilder,
               private authenticationService: AuthenticationService,
               private dialogRef: MatDialogRef<SignUpDialogComponent> ) {
    this.signUpForm = this.formBuilder.group( {
      username: new FormControl(null, [ Validators.required, Validators.nullValidator ] ),
      email: new FormControl( null, [ Validators.required, Validators.email ] ),
      password: new FormControl( null, [ Validators.required ] ),
      passwordRepeat: new FormControl( null ),
    }, { validators: passwordValidator } );

    this.logInForm = this.formBuilder.group( {
      username: new FormControl(null, [ Validators.required, Validators.nullValidator ] ),
      password: new FormControl( null, [ Validators.required, Validators.nullValidator ] ),
    } );
  }

  ngOnInit(): void {
  }

  submitSignUp(): void {
    const { username, email, password } = this.signUpForm.value;
    this.authenticationService.signUp( username, email, password )
      .then( response => {
        console.log( response );
        this.dialogRef.close();
      } )
      .catch( error => {
        console.warn( error );
      } );
  }

  submitLogIn(): void {
    const { username, password } = this.logInForm.value;
    this.authenticationService.logIn( username, password )
      .then( response => {
        console.log( response );
        this.dialogRef.close();
      } )
      .catch( error => {
        console.warn( error );
      } );
  }

}