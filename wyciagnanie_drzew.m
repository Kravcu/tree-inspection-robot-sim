clc
clear
close all

forest = imread("bialowieska.PNG");
[X, Y, Z] = size(forest);

black_white_forest = zeros(X,Y);

for i = 1:X
    for j = 1:Y
        black_white_forest(i,j) = (forest(i,j,1)+forest(i,j,2)+forest(i,j,3))/3;
    end
end

black_white_forest = uint8(black_white_forest);
forest_bin = zeros(X,Y);

for i = 1: X
    for j = 1:Y
        mean_pix = meanLT(i,j,10, black_white_forest, X, Y);
        o_stand = stddevLT(i,j,7,black_white_forest,mean_pix,X,Y);
        thresh = mean_pix*(1+0.15*(o_stand/128 - 1));
        if(black_white_forest(i,j)>thresh)
            forest_bin(i,j) = 0;
        else
            forest_bin(i,j) = 255;
        end
    end
end

indeks1 = forest_bin;
L = 1;
sklejenia = [];
indeks1 = double(indeks1);
[rows, cols] = size(indeks1);

indeks1(1,:) = 0;
indeks1(886,:) =0;
indeks1(:,1) = 0;
indeks1(:,1317) = 0;

for i = 2:rows
    for j = 2:cols-1
        if indeks1(i,j) ~= 0
            neighbours = [indeks1(i,j-1),indeks1(i-1,j-1),indeks1(i-1,j),indeks1(i-1,j+1)];
            if(sum(neighbours)==0)
                indeks1(i,j) = L;
                L = L + 1;
                sklejenia(L) = L;
            elseif(sum(neighbours)>0)
                neighbours = nonzeros(neighbours);
                minimal = min(neighbours);
                maximal = max(neighbours);
                indeks1(i,j) = minimal; 
                if maximal ~= minimal
                    sklejenia(maximal) = minimal;
                end
            end
        end
    end
end

for i = 2:rows
    for j = 1:cols -1
        if indeks1(i,j) ~= 0
            indeks1(i,j) = sklejenia(indeks1(i,j));
        end
    end
end

indeks_final = zeros(886,1317,3);

for i = 1:rows
    for j = 1:cols
        indeks_final(i,j,2) = mod(indeks1(i,j),255);
        indeks_final(i,j,1) = (indeks1(i,j)-mod(indeks1(i,j),255))/255;
    end
end

indeks_final = uint8(indeks_final);

trees = zeros(886,1317);

m00 = zeros(L);
m10 = zeros(L);
m01 = zeros(L);

indeks1 = int32(indeks1);

for i = 1:rows
    for j = 1:cols
        if (indeks1(i,j)~=0)            
            m00(indeks1(i,j)) = m00(indeks1(i,j)) + 1;
            m10(indeks1(i,j)) = m10(indeks1(i,j)) + i;
            m01(indeks1(i,j)) = m01(indeks1(i,j)) + j;
        end
    end
end

x=0;
y=0;

for i = 1:L
    if m00(i)~=0
        x = m10(i)/m00(i);
        y = m01(i)/m00(i);
        x = int32(x);
        y = int32(y);
        trees(x,y) = 1;
    end
end

figure()
subplot(2,2,1)
imshow(forest)
title("oryginalne zdjecie")

subplot(2,2,2)
imshow(forest_bin)
title("binaryzacja oryginalnego zdjęcia")

subplot(2,2,3)
imshow(indeks_final)
title("indeksacja binaryzacji")

subplot(2,2,4)
imshow(trees,[])
title("pnie drzew")

figure
imshow(indeks_final)

figure()
imshow(trees,[])