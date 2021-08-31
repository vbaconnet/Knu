% Génération spectre de Jonswap

% Calcul du spectre de jonswap en fonction de la fréquence et des
% paramètres Hs (Hm0), Tp et gamma

% Note: Il y a deux méthodes pour obtenir le spectre
%       --> Formule avec ajustement du coefficient a par intégration
%       --> Formule dans alea.f
% Pour choisir celle à utiliser, ajuster la variable "type". Si type est
% différent de 1, la méthode sélectionnée par défaut est l'ajustement de a.
% Si type = 1, on sélectionne la méthode de alea.f
function spectre = jonswap(w, Hs, Tp, gamma, type)

    if type ~= 1
        %Calcul du spectre avec a=1 
        spectre_1 = spectreJonswap(1.0, w, Hs, Tp, gamma); 
        
        dw = w(2) - w(1); % Pas de discrétisation
        a = (Hs / 4.0)^2 * (integrale(spectre_1, dw))^(-1); % Calcul de a
        
        % Spectre final
        spectre = spectreJonswap(a, w, Hs, Tp, gamma);
    else
        f = w / (2.0*pi);
        wp = 2.0*pi/Tp;
        fp = wp / (2.0*pi);
        
        betaJ = (0.06238/(0.23+0.0336*gamma-0.185/(1.9+gamma)))* ...
            (1.094-0.01915*log(gamma));
        %disp('betaJ : '  +  betaJ)
        
        expo = exp(-1.25 * ((Tp*f).^(-4.0)) );
        
        gexpo = gamma .^ (exp( -0.5 * (f./fp - 1.0).^2 / (sig(w,wp)^2) ));
        
        spectre = betaJ * Hs * Hs * Tp^(-4.0) * f.^(-5.0) .* expo .* gexpo;
    end
    
end

% Spectre de Jonswap en fonction de la de la fréquence et des
% paramètres Hs (Hm0), Tp et gamma, ainsi que la constante a
function spec = spectreJonswap(a, w, Hs, Tp, gamma)
    wp = 2.0*pi/Tp;  % Pulsation pic
    
    t1 = 2.0*pi * a * Hs^2 * wp^(4) * w.^(-5);     % terme 1
    t2 = exp( -1.25*((w./wp).^(-4)) );    % terme 2
    
    exposant = exp( -0.5 * (w-wp).^2 / (sig(w, wp)^2 * wp^2) );
    t3 = gamma.^exposant;               % terme 3
    
    spec = t1.*t2.*t3;  % Spectre final
end

% Intègre un vecteur avec un pas constant par la méthode des trapèzes
function res = integrale(vec, dx)
    N = length(vec);
    res = sum(vec(2:N) + vec(1:N-1)) * 0.5 * dx;
end

% Renvoie la valeur de sigma selon omega et omega_p
function s = sig(w, wp)
    if w < wp
        s = 0.07;
    else
        s = 0.09;
    end
end