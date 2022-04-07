import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:flutter/material.dart';
import 'package:smarthome/ui/models/customer.dart';

class GoogleSignInProvider extends ChangeNotifier {
  final googleSignIn = GoogleSignIn();
  GoogleSignInAccount? _user;
  GoogleSignInAccount get getUser => _user!;
  var _didSelectUser = false;
  var _tapOnHCMUT = false;
  var _darkMode = false;
  bool get didSelectUser => _didSelectUser;
  bool get didTapOnHCMUT => _tapOnHCMUT;
  bool get darkMode => _darkMode;

  Future googleLogin() async {
    final googleUser = await googleSignIn.signIn();
    if (googleUser == null) return;
    _user = googleUser;
    final googleAuth = await googleUser.authentication;
    final credential = GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );
    await FirebaseAuth.instance.signInWithCredential(credential);
    notifyListeners();
  }

  Future logout() async {
    googleSignIn.disconnect();
    FirebaseAuth.instance.signOut();
    notifyListeners();
  }

  void set darkMode(bool darkMode) {
    _darkMode = darkMode;
    notifyListeners();
  }

  void tapOnHCMUT(bool selected) {
    _tapOnHCMUT = selected;
    notifyListeners();
  }

  void tapOnProfile(bool selected) {
    _didSelectUser = selected;
    notifyListeners();
  }

  final user = FirebaseAuth.instance.currentUser;
  Customer get getCustomer => Customer(darkMode: _darkMode, user: user);
}
