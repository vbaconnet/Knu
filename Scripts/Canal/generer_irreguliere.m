%close all
clc

% Fichier de param�tres 
paramfile = 'params.txt';
fprintf('Lecture des param�tres dans %s \n\n', paramfile)

%==========================================================================
% ------------------------- Lecture des paramètres ------------------------
%==========================================================================

fileID = fopen(paramfile); % ouvrir le fichier param�tres

% Lire coefficients, 9 premi�res lignes
params = textscan(fileID, '%s %f', 9,'CommentStyle','%');  
vals = params{2};

% Lire nom de fichier, 1 ligne suivante
params = textscan(fileID, '%s %s', 2, 'CommentStyle','%');   
fichiers = params{2};

% Lire consignes de generation, 3 lignes suivantes
params = textscan(fileID, '%s %d', 3, 'CommentStyle','%'); 
consignes = params{2};

fclose(fileID); % Fermer le fichier

Tmin = vals(1);
fprintf('Tmin  : %f s\n', Tmin)
Tmax = vals(2);
fprintf('Tmax  : %f s\n', Tmax)
Tp = vals(3);
fprintf('Tp    : %f s\n', Tp)
Hs = vals(4);
fprintf('Hs    : %f m\n', Hs)
gamma = vals(5);
fprintf('gamma : %f \n', gamma)
Ncomposantes = vals(6);
fprintf('\nNombre de composantes      : %d \n', Ncomposantes)
h = vals(7);
fprintf('Hauteur d eau              : %f m\n', h)
duree_simu = vals(8);
fprintf('Duree de simulation        : %f s\n', duree_simu)
rampTime = vals(9);
fprintf('rampe                      : %f s\n', rampTime)

fichier_sortie = char(fichiers(1));
fichier_deph   = char(fichiers(2));
fprintf('\nFichier de sortie : %s \n', fichier_sortie)

% Fichiers .dat et .volts � partir du nom de fichier
fichier_ecriture = strcat(fichier_sortie, '.dat');
fichier_volts    = strcat(fichier_sortie, '.volts');

% Affichage de graphiques
plots = consignes(1);
if plots
    fprintf('Affichage des graphiques \n')
end

% Ecriture de fichiers .dat et .volts
write_file = consignes(2);
if write_file
    fprintf('Sauvegarde des fichiers .dat et .volts \n')
end

% G�n�ration de d�phasages
generer_dephasages = consignes(3);

% Si on ne souhaite pas g�n�rer de nouveaux d�phasages
if ~generer_dephasages
   
    fprintf('Chargement des d�phasages depuis %s\n', fichier_deph);
    % Essayer de les charger depuis le fichier de d�phasages en param�tre
    try
        dephasages = load(fichier_deph);
        fprintf('D�phasages correctement charg�s\n');  
    
    % Si on n'a pas r�ussi � lire, c'est que le chemin n'est pas bon :
    % erreur
    catch
        error('%s : fichier invalide\nV�rifiez le chemin du fichier', fichier_deph);
    end
end

%==========================================================================
% --------------------- G�n�ration du spectre JONSWAP ---------------------
%==========================================================================

deuxpi = 2.0*pi;

% G�n�ration du vecteur de fr�quences
wmin = deuxpi / Tmax;
wmax = deuxpi / Tmin;
w = linspace(wmin, wmax, Ncomposantes);
f = w / deuxpi;
dw = w(2) - w(1);
df = f(2) - f(1);

% Spectre de jonswap
fprintf('\nGeneration du spectre...\n')
spectre = jonswap(w, Hs, Tp, gamma, 0);
fprintf('Ok\n')

fprintf('Generation des amplitudes \n')
% G�n�ration des amplitudes etc
H = 2.0 * sqrt(spectre * dw); % Hauteur de houle
fprintf('Ok \n')

% G�n�ration de d�phasages si besoin
if generer_dephasages
    fprintf('Generation de dephasages \n')
    dephasages = deuxpi .* rand(Ncomposantes,1); % D�phasages entre 0 et 2pi
    fprintf('Ok\n')
end

%=========================================================================
% -------------------------- Mouvement du batteur ------------------------
%=========================================================================

freq_echantillon = 200.0;  % Fr�quence d'�chantillonnage
dt = 1.0/freq_echantillon; % P�riode d'�chantillonnage
Npoints = duree_simu / dt; % Nombre de points d'�chantillon
t = linspace(0.0, duree_simu, Npoints + 1); % Dur�e de simulation

x_batteur = zeros(1, length(t)); % Initialisation du signal du batteur

fprintf('Generation du mouvement du batteur \n')
% Somme des signaux de batteur monochromatiques
for i = 1:Ncomposantes
    x_batteur = x_batteur + deplacement_batteur(t, H(i), deuxpi/w(i), ...
        h, dephasages(i));
end
fprintf('Ok \n')

fprintf('Application des rampes \n')
% Application d'une rampe lin�aire de 10 secondes au d�but
k = t <= rampTime; % Chercher les indices de t o� t < rampTime
x_batteur(k) = t(k)/rampTime .* x_batteur(k); % Appliquer sur ces valeurs

% Application d'une rampe lin�aire rampTime secondes avant la fin
k = t >= duree_simu - rampTime; % Chercher les rampTime secondes avant la fin 
x_batteur(k) = (duree_simu - t(k))/rampTime .* x_batteur(k); % Appliquer sur ces valeurs

fprintf('Ok \n')

%==========================================================================
% ----------------------------- V�rifications -----------------------------
%==========================================================================

fprintf('\nD�placement min : %f mm\n', min(1000*x_batteur))
fprintf('D�placement max : %f mm\n', max(1000*x_batteur))

% V�rifier qu'on a pas atteint la course maximale
if max(abs(x_batteur)) >= 0.3
    fprintf('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    fprintf('+                 !! ATTENTION !!                       +\n')
    fprintf('+ La course maximale du batteur est sup�rieure a 30 cm  +\n')
    fprintf('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
end

% V�rification des vitesses maximales
v_batteur = diff(x_batteur)/dt; % Calcul de vitesse
critere_vitesse = 2.0;

fprintf('Vitesse min : %f m/s\n', min(v_batteur))
fprintf('Vitesse max : %f m/s\n', max(v_batteur))

if max(abs(v_batteur)) >= critere_vitesse
    fprintf('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    fprintf('+                 !! ATTENTION !!                       +\n')
    fprintf('+ Vitesse maximale du batteur sup�rieure � %.2f m/s     +\n', ...
        critere_vitesse)
    fprintf('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
end

a_batteur = diff(v_batteur)/dt;
critere_acc = 1.0;

fprintf('Acceleration min : %f m/s�\n', min(a_batteur))
fprintf('Acceleration max : %f m/s�\n', max(a_batteur))

if max(abs(a_batteur)) >= critere_acc
    fprintf('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    fprintf('+                 !! ATTENTION !!                       +\n')
    fprintf('+ Acc�l�ration max du batteur sup�rieure � %.2f m/s�    +\n', ...
        critere_acc)
    fprintf('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
end

% Conversion en mm
x_batteur = 1000 * x_batteur;

%==========================================================================
% -------------------------------- Sauvegarde -----------------------------
%==========================================================================

% Ecriture dans un fichier s�par�
if write_file
    
    fprintf('\nEcriture du fichier %s \n', fichier_ecriture)
    x_batteur = x_batteur';

    % ------------- Fichier .dat ------------------------------------------
    
    fileID = fopen(fichier_ecriture, 'wt+');
    
    fprintf(fileID, '%f  %d \n', [dt Npoints]); % Ecrire dt et le nb de points
    % et sauvegarder le mouvement du batteur
    save(fichier_ecriture, 'x_batteur', '-ASCII', '-append'); 
    
    fclose(fileID); % Fermer le fichier .dat
    
    fprintf('Ok \n')
    % ------------- Fichier .volts ----------------------------------------
    
    fprintf('Ecriture du fichier %s \n', fichier_volts)
    % Ecrire le fichier .volts
    x_volts = x_batteur * 5.0/300.0;
    save(fichier_volts, 'x_volts', '-ASCII');
    fprintf('Ok \n')
end

fprintf('Fin du programme de g�n�ration \n')

%==========================================================================
% -------------------------------- Trac� ----------------------------------
%==========================================================================

if plots 
    
    % ----------------- Spectre ---------------
    plot(w, spectre);
    xlabel('fr�quence (rad/s)')
    ylabel('S(w) (m�s)')
    
    % --------- Mouvement du batteur ----------
    
    figure()
    hold on
    plot(t, x_batteur);
    plot([0 duree_simu], [max(x_batteur) max(x_batteur)], 'r')
    plot([0 duree_simu], [min(x_batteur) min(x_batteur)], 'r')
    hold off
    xlabel('Temps (s)')
    ylabel('D�placement (mm)')
    xlim([0.0 duree_simu])

end

