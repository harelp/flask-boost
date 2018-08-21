var pieColors = ['rgb(236, 208, 120)', 'rgba(217, 91, 67, 0.7)', 'rgba(192, 41, 66, 0.7)', 'rgba(84, 36, 55, 0.7)', 'rgba(83, 119, 122, 0.7)', 'rgba(119, 146, 174, 0.7)'];

function getTotal( arr ){
    var j,
        myTotal = 0;
    
    for( j = 0; j < arr.length; j++) {
        myTotal += ( typeof arr[j] === 'number' ) ? arr[j] : 0;
    }
    
    return myTotal;
}

function drawPieChart( canvasId ) {
    var i,
        canvas = document.getElementById( canvasId ),
        pieData = canvas.dataset.values.split(',').map( function(x){ return parseInt( x, 10 )}),
        halfWidth = canvas.width * .5,
        halfHeight = canvas.height * .5,
        ctx = canvas.getContext( '2d' ),
        lastend = 0,
        myTotal = getTotal(pieData);

    ctx.clearRect( 0, 0, canvas.width, canvas.height );

    for( i = 0; i < pieData.length; i++) {
        ctx.fillStyle = pieColors[i];
        ctx.beginPath();
        ctx.moveTo( halfWidth, halfHeight );
        ctx.arc( halfWidth, halfHeight, halfHeight, lastend, lastend + ( Math.PI * 2 * ( pieData[i] / myTotal )), false );
        ctx.lineTo( halfWidth, halfHeight );
        ctx.fill();
        lastend += Math.PI * 2 * ( pieData[i] / myTotal );
    }
}

drawPieChart('canPie');

var pieColors = ['rgb(236, 208, 120)', 'rgba(217, 91, 67, 0.7)', 'rgba(192, 41, 66, 0.7)', 'rgba(84, 36, 55, 0.7)', 'rgba(83, 119, 122, 0.7)', 'rgba(119, 146, 174, 0.7)'];

function getTotal( arr ){
    var j,
        myTotal = 0;
    
    for( j = 0; j < arr.length; j++) {
        myTotal += ( typeof arr[j] === 'number' ) ? arr[j] : 0;
    }
    
    return myTotal;
}

function drawPieChart( canvasId ) {
    var i,
        canvas = document.getElementById( canvasId ),
        pieData = canvas.dataset.values.split(',').map( function(x){ return parseInt( x, 10 )}),
        halfWidth = canvas.width * .5,
        halfHeight = canvas.height * .5,
        ctx = canvas.getContext( '2d' ),
        lastend = 0,
        myTotal = getTotal(pieData);

    ctx.clearRect( 0, 0, canvas.width, canvas.height );

    for( i = 0; i < pieData.length; i++) {
        ctx.fillStyle = pieColors[i];
        ctx.beginPath();
        ctx.moveTo( halfWidth, halfHeight );
        ctx.arc( halfWidth, halfHeight, halfHeight, lastend, lastend + ( Math.PI * 2 * ( pieData[i] / myTotal )), false );
        ctx.lineTo( halfWidth, halfHeight );
        ctx.fill();
        lastend += Math.PI * 2 * ( pieData[i] / myTotal );
    }
}

drawPieChart('canPie1');

var pieColors = ['rgb(236, 208, 120)', 'rgba(217, 91, 67, 0.7)', 'rgba(192, 41, 66, 0.7)', 'rgba(84, 36, 55, 0.7)', 'rgba(83, 119, 122, 0.7)', 'rgba(119, 146, 174, 0.7)'];

function getTotal( arr ){
    var j,
        myTotal = 0;
    
    for( j = 0; j < arr.length; j++) {
        myTotal += ( typeof arr[j] === 'number' ) ? arr[j] : 0;
    }
    
    return myTotal;
}

function drawPieChart( canvasId ) {
    var i,
        canvas = document.getElementById( canvasId ),
        pieData = canvas.dataset.values.split(',').map( function(x){ return parseInt( x, 10 )}),
        halfWidth = canvas.width * .5,
        halfHeight = canvas.height * .5,
        ctx = canvas.getContext( '2d' ),
        lastend = 0,
        myTotal = getTotal(pieData);

    ctx.clearRect( 0, 0, canvas.width, canvas.height );

    for( i = 0; i < pieData.length; i++) {
        ctx.fillStyle = pieColors[i];
        ctx.beginPath();
        ctx.moveTo( halfWidth, halfHeight );
        ctx.arc( halfWidth, halfHeight, halfHeight, lastend, lastend + ( Math.PI * 2 * ( pieData[i] / myTotal )), false );
        ctx.lineTo( halfWidth, halfHeight );
        ctx.fill();
        lastend += Math.PI * 2 * ( pieData[i] / myTotal );
    }
}

drawPieChart('canPie2');
