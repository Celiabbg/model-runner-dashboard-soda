import React, { useEffect, useState } from 'react';
import { PublicClientApplication, InteractionType, AccountInfo } from '@azure/msal-browser';
import { msalConfig } from '../auth/msal';

const msalInstance = new PublicClientApplication(msalConfig);

export default function LoginGate({ children }: { children: React.ReactNode }) {
  const [account, setAccount] = useState<AccountInfo | null>(null);

  useEffect(() => {
    msalInstance.handleRedirectPromise().then(() => {
      const acc = msalInstance.getAllAccounts()[0];
      if (acc) setAccount(acc);
      else msalInstance.loginRedirect({ scopes: ['User.Read'] });
    });
  }, []);

  if (!account) return <div>Redirecting to login...</div>;
  return <>{children}</>;
}