% Margins

% SPECIFY RATIO
RATIO_HEIGHT = 9;
RATIO_WIDTH = 16;

% READ FILES
files = dir('*.png');

% START
clc
for f=1:size(files)
    % READ FILE
    IMG = imread(files(f).name);
    [h w d] = size(IMG);

    % CALCULATE RATIO
    ratio = w/h;

    % PRINT FILENAME
    fprintf('\n\n-------------------------------------');
    fprintf('\n# PROCESSING FILE: \t%s', files(f).name);

    % PRINT ORIENTATION
    if(h > w)
        orientation = 1;
        fprintf('\nPORTRAIT');
    else
        orientation = 2;
        fprintf('\nLANDSCAPE');
    end

    % PRINT DIMENSIONS
    fprintf('\t|\t%i x %i', h, w);

    % CHECK RATIO?
    if(h/w == RATIO_HEIGHT/RATIO_WIDTH)
        fprintf('\n > Correct aspect ratio.');
        NIMG = IMG;        
    else
        fprintf('\n! BAD aspect ratio : %f', h/w);

        % CALCULATE NEW DIMENSIONS
        if(ratio < RATIO_WIDTH/RATIO_HEIGHT)
            ch = h;
            cw = round(RATIO_WIDTH/RATIO_HEIGHT*ch);
        else
            cw = w;
            ch = round(RATIO_HEIGHT/RATIO_WIDTH*cw);
        end

        % PRINT NEW DIMENSIONS
        fprintf('\nNEW DIMENSIONS: \t%i x %i | ADDED: %i x %i', ch, cw, ch-h, cw-w);

        % CREATE NEW IMAGE
        NIMG = uint8(ones(ch,cw,d)*255);

        % COPY
        for k=1:d
            for i=1:h
                for j=1:w
                    NIMG(i,round(j+((cw-w)/2)),k) = IMG(i,j,k);
                end
            end
        end
    end

    % WRITE
    imwrite(NIMG, ['modified\' files(f).name '.png'], 'png');
end