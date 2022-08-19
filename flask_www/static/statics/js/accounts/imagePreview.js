"use strict"
/*jshint esversion: 6 */
imgPreviewInit();
function imgPreviewInit() {
    try {
        const profileImgInput = document.querySelector("#profile_image");
        profileImgInput.addEventListener("change", function (e) {
            let _width = `100%`;
            let _height = `100%`;
            let profileImgPreviewTag = document.querySelector('#img-preview');
            previewStyle(profileImgPreviewTag, _width, _height);

            let profileImgInputFile = document.querySelector('#profile_image').files[0];
            imgFileReader(profileImgPreviewTag, profileImgInputFile);
        }, false);
    } catch (e) {
        console.log(e);
    }

    try {
        const corpImgInput = document.querySelector("#corp_image");
        corpImgInput.addEventListener("change", function (e) {
            let _width = `100%`;
            let _height = `500px`;
            let corpImgPreviewTag = document.querySelector('#corp-img-preview');
            previewStyle(corpImgPreviewTag, _width, _height);

            let corpImgInputFile = document.querySelector('#corp_image').files[0];
            imgFileReader(corpImgPreviewTag, corpImgInputFile);
        }, false);
    } catch (e) {
        console.log(e);
    }

    try {
        const coverImgInput = document.querySelector("#cover_image");
        coverImgInput.addEventListener("change", function (e) {
            let _width = `100%`;
            let _height = `500px`;
            let coverImgPreviewTag = document.querySelector('#cover-img-preview');
            previewStyle(coverImgPreviewTag, _width, _height);

            let coverImgInputFile = document.querySelector('#cover_image').files[0];
            imgFileReader(coverImgPreviewTag, coverImgInputFile);
        }, false);
    } catch (e) {
        console.log(e);
    }

}

function previewStyle(previewImgTag, _width, _height) {
    previewImgTag.style.cssText = ` width:` + _width + `;
                                height:` + _height + `;
                                object-fit:cover;
                                `;
}

function imgFileReader(previewImgTag, inputFile) {
    let reader = new FileReader();
    reader.addEventListener("load", function () {
        previewImgTag.src = reader.result;
    }, false);

    if (inputFile) {
        previewImgTag.classList.add('active');
        console.log('inputFile.name:::', inputFile.name);
        reader.readAsDataURL(inputFile);
    } else {
        // previewImgTag.classList.remove('active');
        // previewImgTag.style.display = "none";
        window.location.reload();
    }
}


