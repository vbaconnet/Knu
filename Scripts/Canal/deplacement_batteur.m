% G�n�rer un signal de d�placement de batteur � partir de param�tres de 
% houle monochromatique:
%   - t : vecteur de temps
%   - H : Hauteur de houle
%   - T : P�riode de houle
%   - h : hauteur d'eau
%   - phi : d�phasage

% Formule de conversion houle <-> batteur issue de :
% [Advanced series on ocean engineering 2] Robert G. Dean, 
% Robert A. Dalrymple - Water wave mechanics for engineers and scientists 
%(1991, World Scientific)
% Consultable dans : T:\Services\Production\Sophia\Modelisation_Physique\_DOCUMENTATION

% La formule utilis�e pr�c�demment dans alea.f est:
% tau = 2 * tanh(k*h) / (1 + k*h*(1 - tanh(k*h)*tanh(k*h))/tanh(k*h);
function x = deplacement_batteur(t, H, T, h, phi)

    L = dispersion(T,h); % Calcul de longueur d'onde
    k = 2.0 * pi / L;    % Nombre d'onde
    w = 2.0 * pi / T;    % Fr�quence en rad/s

    tau = 2* (cosh(2*k*h) - 1) / (sinh(2*k*h) + 2*k*h);
    
    x = H/tau * cos(-w.*t + phi); %Signal du batteur
end

% Calcule la longueur d'onde � partir de la p�riode de houle et hauteur
% d'eau gr�ce � la relation de dispersion. 
% 
% Le calcul se fait par m�thode du point fixe sur 100 it�rations ou si une 
% pr�cision de 1e-3 est atteinte.
function L = dispersion(T,h)

    L0 = 9.81 * T^2 / (2.0*pi);
    L = L0;
    Lnew = L0 * tanh(2.0*pi/L*h);
    
    N = 0;
    while abs(Lnew - L) > 0.001 && N < 100
        L = Lnew;
        Lnew = L0 * tanh(2.0*pi/L*h);
        N = N+1;
    end
end